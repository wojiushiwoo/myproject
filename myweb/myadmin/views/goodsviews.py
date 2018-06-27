from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse

# 可以选择导入gettypesorder，也可以复制到本页，简单修改后使用
from . typesviews import gettypesorder
from . userviews import uploads
from .. models import Goods,Types,Users
import os
# Create your views here.
def uploads(request):
    # 获取请求的 文件 File
    myfile = request.FILES.get('pics', None)

    # 获取上传的文件后缀名 myfile.name.split('.').pop()
    p = myfile.name.split('.').pop()
    arr = ['jpg','png','jpeg', 'gif']

    if p not in arr :
        return 1

    import time, random
    # 生成新的文件名
    filename = str(time.time()) + str(random.randint(1,9999)) + '.' + p

    # 打开文件
    destination = open("./static/pics/" + filename, "wb+")

    # 分块写入文件
    for chunk in myfile.chunks():
        destination.write(chunk)

    # 关闭文件
    destination.close()

    return '/static/pics/' + filename 
def add(request):
    if request.method == 'GET':
        glist = gettypesorder()
        context = {'glist':glist}

        return render(request,'myadmin/goods/add.html',context)

    elif request.method == 'POST':
        # 先判断是否有图片上传
        # if not request.FILES.get('pics',None):
        #     return HttpResponse('<script>alert("必须选择商品图片");location.href="'+reverse('myadmin_goods_add')+'"</script>')

        pics = uploads(request)
        if pics == 1:
            return HttpResponse('<script>alert("图片类型有误");location.href="'+reverse('myadmin_goods_add')+'"</script>')

        # 执行商品的添加
        # 接收表单提交的数据，
        data = request.POST.copy().dict()
        # 同user表，删除掉 csrf验证的字段数据，否则数据长度对不上报错
        del data['csrfmiddlewaretoken']

        data['pics'] = pics
        data['typeid'] = Types.objects.get(id = data['typeid'])

        # 执行用户的创建,create具有保存功能
        ob = Goods.objects.create(**data)

        # 需要改成一个地址
        return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_goods_list')+'"</script>')

def index(request):
    glist = Goods.objects.all()

    context = {'glist':glist}

    return render(request, 'myadmin/goods/list.html',context)

def delete(request):
    try: 
        gid = request.GET.get('gid',None)

        # # 判断当前类下是否有子类,types中pid父级，gid获取的request.GET.get（）对象的'gid'的值
        # types中还要判断goods中是否有商品
        # num = Goods.objects.filter(id = gid).count()
        ob = Goods.objects.get(id = gid)
       # 删除的ob是一整条数据
        ob.delete()

        data = {'msg':'删除成功', 'code':0}
    except:
        data = {'msg':'删除失败', 'code':1}
    return JsonResponse(data)

def edit(request):
    # 分类不允许随便删，所以，对应地也不可以随便修改，给管理员用的，不是用户用的
    # 一般只允许修改名字，获取名字，修改名字即可
    # 这个gid是用户点击修改获得所在objects的id，?gid={{ uinfo.id }}
    gid = request.GET.get('gid',None)
    # if not gid:
    #     return HttpResponse('<script> alert("没有用户数据"); location.href ="'+reverse("myadmin_types_list")+'"</script>')

    # 获取对象

    # 当前的gid必须是变量才能这么写
    ob = Goods.objects.get(id = gid)

    if request.method == 'GET':
        # 分配数据，讲数据放到列表上，默认数据
        
        glist = gettypesorder()
        # context = {'glist':glist}
        context = {'ginfo':ob,'glist':glist}
        # 显示编辑页面，数据放在编辑页面作为默认数据
        return render(request,'myadmin/goods/edit.html',context)


    elif request.method == 'POST':
        # try:
        if request.FILES.get('pics',None):
            # 判断是否使用的默认图
            if ob.pics:
                # 如果使用的不是默认图,则删除之前上传的头像
                os.remove('.'+ob.pics)

            # 执行上传
            ob.pics = uploads(request)
            

        # ob.typeid = request.POST['typeid']
        ob.title = request.POST['title']
        ob.descr = request.POST['descr']
        ob.info = request.POST['info']
        ob.price = request.POST['price']
        ob.store = request.POST['store']
        # ob.num = request.POST['num']
        ob.save()

        return HttpResponse('OK')
            # return HttpResponse('<script> alert("修改成功"); location.href ="'+reverse("myadmin_types_list")+'"</script>')
        # except:
        #     return HttpResponse('<script> alert("修改失败"); location.href ="'+reverse("myadmin_types_edit")+"?gid="+str(ob.id)+'"</script>')




