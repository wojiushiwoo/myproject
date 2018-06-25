from django.shortcuts import render
from django.http import HttpReponse

# Create your views here.
def index(request):
    return render(request, 'myadmin/index.html')