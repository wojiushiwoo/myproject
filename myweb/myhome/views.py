from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):

    return HttpResonse('前台页面')