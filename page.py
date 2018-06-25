def page(count,p):
    # count 总页数
    # 当前的页码数
    if count>10:
        if p<=5 :
            start = 1
            end = 10
        elif p>=count-5:
            start = count-10
            end = count
        else:
            start = p-4
            end = p+5

    else:
        start = 1
        end = count

    for i in range(start,end+1):
        print(i)
       
page(6,3)
