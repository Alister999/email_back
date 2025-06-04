from django.http import HttpResponseServerError
from django.shortcuts import render

def show_start(request):
    return render(request, 'main_page/index.html')

def error_view(request):
    return HttpResponseServerError()
    # raise Exception("Test error")
