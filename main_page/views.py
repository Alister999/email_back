from http.client import HTTPException

from django.http import HttpRequest, HttpResponse, HttpResponseServerError
from django.shortcuts import render

# Create your views here.

def show_start(request):
    return render(request, 'main_page/index.html')

def error_view(request):
    return HttpResponseServerError()#HttpResponse()
