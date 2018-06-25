

项目目录结构

py
├── manage.py 入口文件
├── myadmin    后台应用
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py 后台模型       
│   ├── tests.py
│   ├── urls.py 后台路由
│   └── views 后台应用的视图文件目录
│       ├── goodsviews.py   商品的视图
│       ├── orderviews.py   订单视图
│       ├── typeviews.py    分类试图
│       ├── userviews.py    会员试图
│       └── views.py        后台视图
├── myhome       前台应用          
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py  前台模型
│   ├── tests.py
│   ├── urls.py  前台的路由
│   └── views.py  前台的视图
├── py           与项目同名目录,django的配置目录
│   ├── __init__.py
│   ├── settings.py   配件文件
│   ├── urls.py       根 路由
│   └── wsgi.py       
├── static           静态文件目录
│   ├── myadmin     
│   │   ├── css
│   │   ├── fonts
│   │   ├── img
│   │   └── js
│   └── myhome
└── templates      模板目录
    ├── myadmin
    │   ├── index.html
    │   └── public
    │       └── base.html
    └── myhome
        └── index.html



会员管理:
    添加,列表,删除,修改,搜索,分页





