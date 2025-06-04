"""URLs apps module"""
from django.urls import path

from main_page.views import show_start, error_view

urlpatterns = [
    path('', show_start),
    path('error', error_view, name='error')
]
