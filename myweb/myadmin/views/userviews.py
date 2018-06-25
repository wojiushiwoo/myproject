from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse

from .. models import Users
import os

# 会员列表
def index(request):

    # 获取搜索条件
    types = request.GET.get('type', None)
    keywords = request.GET.get('keywords', None)

    # 判断搜索条件是否有？如果有，是否成立
    if types:

        from django.db.models import Q
        if types == 'all':
            # 全条件搜索 django软件内置有模块Q ，方法 val__contains(a)
            # <=> select * from user where username like '%a%';
            userlist = Users.objects.filter(
                Q(username__contains = keywords)|
                Q(age__contains = keywords)|
                Q(email__contains = keywords)|
                Q(phone__contains = keywords)|
                Q(sex__contains = keywords)
                )

        # 分别按照用户名、年龄等等子选项搜索
        elif types == 'username':
            userlist = Users.objects.filter(username__contains = keywords)
        elif types == 'age':
            userlist = Users.objects.filter(age__contains = keywords)
        elif types == 'email':
            userlist = Users.objects.filter(email__contains = keywords)
        elif types == 'phone':
            userlist = Users.objects.filter(phone__contains = keywords)
        elif types == 'sex':
            userlist = Users.objects.filter(sex__contains = keywords)

    else:
        # 那么表示输入有误，直接返回所有用户数据
        userlist = Users.objects.filter()

    # 可选择排序条件
    # userlist = userlist.order_by('-id') 

    # 导入django自带的分页类
    from django.core.paginator import Paginator
    # 实例化分页对象，参数1，数据集合，参数2 每页显示条数
    paginator = Paginator(userlist,10)
    # 获取当前页码数
    p = request.GET.get('p', 1)
    # 获取当前页的数据
    ulist = paginator.page(p)
    
    # 分配数据
    context = {'userlist':ulist}
    # 加载模板
    return render(request, 'myadmin/user/list.html',context)

# 会员添加
def add(request):
    if request.method == 'GET':
        # 显示添加页面
        return render(request,'myadmin/user/add.html')

    elif request.method == 'POST':
        # 执行数据添加
        try:
            # 接收表单提交的数据
            data = request.POST.copy().dict()
            # 删除掉 csrf验证的字段数据,该数据在data内属于后续不需要的数据，如果不删除会导致后续 **data 获取数据出错
            del data['csrfmiddlewaretoken']
            print(data)
            # 进行密码加密
            from django.contrib.auth.hashers import make_password,check_password
            data['password'] = make_password(data['password'], None, 'pbkdf2_sha256')

            #  进行头像的上传
            if request.FILES.get('pic',None):
                data['pic'] = uploads(request)
                if data['pic'] == 1:
                    return HttpReponse('<script>alert("上传图片类型有误)"; location.href ="'+reverse("myadmin_user_add")+'"</script>')
            else:
                # 如果不上传，有默认值
                del data['pic']

            # 执行用户的创建
            ob = Users.objects.create(**data)
            # return HttpResponse("OK")
            return HttpResponse('<script> alert("添加成功"); location.href ="'+reverse("myadmin_user_list")+'"</script>')
        except:
            return HttpResponse('<script> alert("添加失败"); location.href ="'+reverse("myadmin_user_add")+'"</script>')

# 会员删除
def delete(request):
    try:  
        uid = request.GET.get('uid',None)
        ob = Users.objects.get(id = uid)

        # 判断当前用户是否有头像，如果有则删除
        if ob.pic:
            # 删除文件，用os模块,已上传的图片是一个文件
            os.remove('.' + ob.pic)
        ob.delete()

        data = {'msg':'删除成功', 'code':0}
    except:
        data = {'msg':'删除失败', 'code':1}

    return JsonResponse(data)

# 显示编辑和执行对象
def edit(request):
    # 接收参数
    uid = request.GET.get('uid', None)
    #  获取对象
    ob = Users.objects.get(id= uid)
    print(ob)
    if request.method == 'GET':
        # 分配数据
        context = {'uinfo':ob}
        return render(request,'myadmin/user/edit.html',context)
    
    
    elif request.method =='POST':
        try:
            # 判断是否有新的图片上传
            if request.FILES.get('pic',None):
                # 判断是否使用的不是默认图，是则删除前途
                if ob.pic:
                    os.remove('.' + ob.pic)

                # 执行上传
                ob.pic = uploads(request)

            ob.username = request.POST['username']
            ob.email = request.POST['email']
            ob.age = request.POST['age']
            ob.sex = request.POST['sex']
            ob.phone = request.POST['phone']
            ob.save()

            return HttpResponse('<script>alert("更新成功"); location.href ="'+reverse("myadmin_user_list")+'"</script>')
        except:
            return HttpResponse('<script> alert(更新失败"); location.href ="'+reverse("myadmin_user_edit")+'?uid='+str(ob.id)+'"</script>')



# 执行文件的上传 图片、视频上传需要改为二进制
def uploads(request):
    # 获取请求的 文件 File
    myfile = request.FILES.get('pic', None)

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