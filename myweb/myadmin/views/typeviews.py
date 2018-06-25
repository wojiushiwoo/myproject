from django.shortcuts import render,reverse
from django.http import HttpReponse,JsonResponse
from .. models import Types

# Create your views here.
def add(request):
    if request.method == 'GET':
        # 返回一个添加的页面
        return render(request, 'myadmin/types/add.html')
    elif request.method == 'POST':
        # 执行分类的添加
        pass

def index(request):
        return render(request, 'myadmin/types/list.html')
    

def delete(request):
    pass

def edit(request):
    pass





