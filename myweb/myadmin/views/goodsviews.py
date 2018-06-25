from django.shortcuts import render,reverse
from django.http import HttpsReponse

# 可以选择导入gettypesorder，也可以复制到本页，简单修改后使用
from . typesviews import gettypesorder
from . userviews import uploads

from .. models import Goods,Types
# Create your views here.

def add(request):
    if request.method == 'GET':
        glist = gettypesorder()
        context = {'glist':glist}

        return render(request,'myadmin/goods/add.html',context)
    elif request.method =='POST':
        # 先判断是否有图片上传
        if not request.FILES.get('pic',None):
            return HttpResponse('<script>alert("必须选择商品图片");location.href="'+reverse('myadmin_goods_add')+'"</script>')

        pic = uploads(request)
        if pic == 1:
            return HttpResponse('<script>alert("图片类型有误");location.href="'+reverse('myadmin_goods_add')+'"</script>')

        # 执行商品的添加
        # 接收表单提交的数据，
        data = reqeust.POST.copy().dict()
        # 同user表，删除掉 csrf验证的字段数据，否则数据长度对不上报错
        del data['csrfmiddlewaretoken']

        data['pics'] = pic
        data['typeid'] = Types.objects.get(id = data['typeid'])

        # 执行用户的创建
        ob = Goods.objects.create(**data)

        # 需要改成一个地址
        return HttPResponse('post')

def index(request):
    glist = Goods.objects.all()

    context = {'glist':glist}

    return render(request, 'myadmin/index.html',context)

def delete(request):
    pass

def edit(request):
    pass



