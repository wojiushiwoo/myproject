from django import template
from django.utils.html import format_html

register = template.Library()

#  自定义页面优化显示标签
@register.simple_tag

def PageShow(count,request):
    p = int(request.GET.get('p', 1))

    # 开始页
    begin = p-4
    # 结束页
    end = p+5

    # 判断如果当前页， 如果小于5

    if p < 5:
        # 则开始页为1
        begin = 1
        # 结束页理论上为 10，可能总数不到10页
        end = 10

    if  p > count-5:
        # 开始总页数为总页数-9,前提是不为负数
        begin = count - 9
        end=count
        # 此时总页数为10

    # 判断，如果开始页小于1 , 则设置开始页为1
    if begin <= 0:
        begin = 1

    # 拼接当前请求的参数 '&keywords=11&type=all'
    u =''
    for x in request.GET:
        # 排除p参数
        if x != 'p':
            u += '&'+x+'='+request.GET[x]

    s = ''
    s += '<li><a href="?p=1'+u+'">首页</a></li>'
    if p - 1 <= 0:
        s += '<li class="am-disabled"><a href="?p=1'+u+'">上一页</a></li>'
    else:
        s += '<li><a href="?p='+str(p-1)+u+'">上一页</a></li>'  

    for x in range(begin,end+1):
        # 判断是否为当前页,当前页要高亮am-active，和非当前页区分开
        if p == x:
            s += '<li class="am-active"><a href="?p='+str(x)+u+'">'+str(x)+'</a></li>'
        else:
            s += '<li ><a href="?p='+str(x)+u+'">'+str(x)+'</a></li>'

    if p+1 >= count:
        s += '<li class="am-disabled"><a href="?p='+str(count)+u+'">下一页</a></li>'
    else:
        s += '<li><a href="?p='+str(p+1)+u+'">下一页</a></li>'

    s += '<li ><a href="?p='+str(count)+u+'">尾页</a></li>'

    # 必须用format_html，否则不解析
    return format_html(s)