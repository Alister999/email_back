from django.urls import path

from main_page.views import show_start

urlpatterns = [
    path('', show_start),
    # path('/error', )
]