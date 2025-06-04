import uuid
from django.utils.log import AdminEmailHandler
from django.core.mail import mail_admins
from django.views.debug import ExceptionReporter
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ChunkedAdminEmailHandler(AdminEmailHandler):
    def emit(self, record):
        if not hasattr(record, 'request'):
            logger.debug("Log without request")
            return

        try:
            request = record.request
            subject = f"{settings.EMAIL_SUBJECT_PREFIX}{record.getMessage()} {uuid.uuid4()}"

            exc_info = record.exc_info if record.exc_info else (None, None, None)
            reporter = ExceptionReporter(request, *exc_info)

            message = reporter.get_traceback_text()

            logger.debug(f"Length of message: {len(message)} characters")

            chunk_size = 5000
            chunks = [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]

            logger.debug(f"Count of parts: {len(chunks)}")

            for i, chunk in enumerate(chunks):
                try:
                    mail_admins(
                        subject=f"{subject} (часть {i+1}/{len(chunks)})",
                        message=f"Путь: {request.path}\n\n{chunk}",
                        fail_silently=False,
                    )
                    logger.debug(f"Letter {i+1}/{len(chunks)} send success!")
                except Exception as e:
                    logger.error(f"Error during send letter {i+1}: {str(e)}")

        except Exception as e:
            logger.error(f"Error in ChunkedAdminEmailHandler: {str(e)}")