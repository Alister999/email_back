"""Utils module for cutting message error"""
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
import aiosmtplib
from django.utils.log import AdminEmailHandler
from django.core.mail import EmailMessage
from django.views.debug import ExceptionReporter
from django.conf import settings

logger = logging.getLogger(__name__)

_executor = ThreadPoolExecutor(max_workers=2)


async def send_email_async(subject, message, from_email, recipient_list):
    """
    Асинхронная отправка письма через aiosmtplib.
    """
    try:
        smtp = aiosmtplib.SMTP(
            hostname=settings.EMAIL_HOST,
            port=int(settings.EMAIL_PORT),
            use_tls=False,
            start_tls=True,
            validate_certs=True,
        )
        await smtp.connect()
        if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            await smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list,
        )
        await smtp.send_message(email.message())
        await smtp.quit()
        logger.debug("Async letter was send: %s", subject)
    except Exception as e:
        logger.error("Error during sending of async letter: %s", str(e))
        raise


def run_async_in_thread(coro):
    """
    Запускает асинхронную корутину в отдельном потоке.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(coro)
    finally:
        loop.close()


class ChunkedAdminEmailHandler(AdminEmailHandler):
    """Cutting message class"""
    def emit(self, record):
        if not hasattr(record, 'request'):
            logger.debug("Log without request")
            return

        try:
            subject = f"{settings.EMAIL_SUBJECT_PREFIX}{record.getMessage()}"

            exc_info = record.exc_info if record.exc_info else (None, None, None)
            reporter = ExceptionReporter(record.request, *exc_info)
            message = reporter.get_traceback_text()

            logger.debug("Length of message: %s characters", len(message))

            chunk_size = 5000
            chunks = [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]

            logger.debug("Count of parts: %s", len(chunks))

            recipient_list = [email for _, email in getattr(settings, 'ADMINS', [])]
            if not recipient_list:
                recipient_list = [settings.SERVER_EMAIL]

            for i, chunk in enumerate(chunks):
                chunk_subject = f"{subject} (part {i + 1}/{len(chunks)})"
                chunk_message = f"Path: {record.request.path}\n\n{chunk}"

                coro = send_email_async(
                    subject=chunk_subject,
                    message=chunk_message,
                    from_email=settings.SERVER_EMAIL,
                    recipient_list=recipient_list,
                )
                _executor.submit(run_async_in_thread, coro)

        except Exception as e:
            logger.error("Error in ChunkedAdminEmailHandler: %s", str(e))
