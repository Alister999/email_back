"""Views module"""
from django.http import HttpResponseServerError
from django.shortcuts import render

def show_start(request):
    """Start view function"""
    return render(request, 'main_page/index.html')

def error_view(request):
    """View function for generating error"""
    return HttpResponseServerError()
    # raise Exception("Test error")
