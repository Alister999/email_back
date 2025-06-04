"""Default apps module"""
from django.apps import AppConfig


class MainPageConfig(AppConfig):
    """Default main page config class"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_page'
