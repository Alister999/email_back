from django.shortcuts import render

# Create your views here.

def show_start(request):
    return render(request, 'main_page/index.html')
