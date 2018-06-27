from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from .. models import Types


# 获取所有的分类信息，由于需要重复利用，写成函数调用
def gettypesorder(): 
    # 使用方法 Types.objects.all()

    # 排序时需要按照path-->id 的主次顺序排序，在数据库中可以二次排序，在这里最好拼接后排序,
    # slelect *,contat(path,id) as paths from myadmin_types order by paths;
    # tlist = Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')
    tlist = Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')
    # tlist = Types.objects.all()
    # 上一列数据虽然得到了tlist，但是显示的效果不好，且pid一项显示为数字，不符合要求
    # tlist代表获取了所有的数据，extra允许允许加入一个额外的字段paths，后又按照paths排序
    for x in tlist:
        if x.pid == 0:
            # pid取值为0 1 2 3，对应的加入数据pname，确定pid父级代表什么，顶级分类没有父级
            x.pname = '顶级分类'

        else:
            t = Types.objects.get(id=x.pid)
            # name 时本身定义好的字段，
            x.pname = t.name
        # 确认了所有的pname与pid的对应关系，还希望显示效果更容易看懂，每增加一级，加|----
        # x.path是字符串
        num = x.path.count(',')-1
        x.name = (num*'|----')+x.name

    return tlist



# Create your views here.
def add(request):
    if request.method == 'GET':
        # 扔给对方一个添加的页面，但是要写明数据对应的关系，最后接收的是tlist，tlist与输入的各项有什么关系，通过下面的代码以及add.html写清楚
        tlist = gettypesorder()

        # 分配数据，因为render第三个参数必须为object
        context = {'tlist':tlist}
        # 返回一个添加的页面
        return render(request,'myadmin/types/add.html',context)

    elif request.method == 'POST':
        # 执行分类的添加,实例化Types
        ob = Types()
        ob.name = request.POST['name']
        ob.pid = request.POST['pid']
        print(ob.pid)
        try:
            if ob.pid == '0':
                ob.path = '0,'
            else:
                # 根据当前父级id获取path,再添加当前父级id,path的值是根据id,pid拼接出来的
                # 不能ob.objects , 因为ob在这里代表一个实例,Types.objects.get()可以认为也是一个实例对象
                t = Types.objects.get(id = ob.pid)
                ob.path = t.path+str(ob.pid)+','
            ob.save()

            return HttpResponse('<script> alert("添加成功"); location.href ="'+reverse("myadmin_types_list")+'"</script>')
        except:
            return HttpResponse('<script> alert("添加失败"); location.href ="'+reverse("myadmin_types_add")+'"</script>')



def index(request):

    tlist = gettypesorder()
    # tlist = Types.objects.all()
    print(type(tlist))
    context = {'tlist':tlist}
    return render(request, 'myadmin/types/list.html', context)
    
    

def delete(request):
    tid = request.GET.get('tid',None)

    # 判断当前类下是否有子类,pid父级，tid获取的request.GET.get（）对象的'uid'的值
    num = Types.objects.filter(pid = tid).count()

    if num !=0:
        data = {'msg':'当前类下有子类，不能删除', 'code':1}
    else:
        # 当后续部分写完后，需要判断当前类下是否有商品，
        
        ob = Types.objects.get(id = tid)
        # 删除的ob是一整条数据
        ob.delete()

        data = {'msg':'删除成功', 'code':0}

    return JsonResponse(data)

def edit(request):
    # 分类不允许随便删，所以，对应地也不可以随便修改，给管理员用的，不是用户用的
    # 一般只允许修改名字，获取名字，修改名字即可
    # 这个tid是用户点击修改获得所在objects的id，?tid={{ uinfo.id }}
    tid = request.GET.get('tid',None)
    if not tid:
        return HttpResponse('<script> alert("没有用户数据"); location.href ="'+reverse("myadmin_types_edit")+'"</script>')

    # 获取对象

    # 当前的tid必须是变量才能这么写
    ob = Types.objects.get(id = tid)

    if request.method == 'GET':
        # 分配数据，讲数据放到列表上，默认数据
        if ob.pid == 0:
            ob.pname = '顶级菜单'
        else:
            ob.pname = Types.objects.get(id = ob.pid).name
        context = {'uinfo':ob}
        # 显示编辑页面，数据放在编辑页面作为默认数据
        return render(request,'myadmin/types/edit.html',context)
        # return HttpResponse('edit')


    elif request.method == 'POST':
        try:
            ob.name = request.POST['name']
            ob.save()

            return HttpResponse('<script> alert("修改成功"); location.href ="'+reverse("myadmin_types_list")+'"</script>')
        except:
            return HttpResponse('<script> alert("修改失败"); location.href ="'+reverse("myadmin_types_edit")+"?tid="+str(ob.id)+'"</script>')





