# 基于URL识别恶意访问系统的设计与实现 

### 一、Features

* Django backend in `./backend`
* vuejs (v2) frontend in `./frontend`
* Hot-reload with vue-loader
* eslint linter integration
* Makefile to make your life easy

### 二、相关命令 
#### 1. 安装项目
    make dev: 安装依赖
    make migrate: 创建数据库

#### 2. 运行项目 
    make run命令分解：
    1) npm run dev: 在8001端口启动vue
    2) python ./manage runserver: 在8000端口运行django
    3) 访问http://localhost:8000/
    //TODO1:目前make run命令执行了前一半就卡住了，2)中的命令无法被执行


### 三、部署 

These steps will install production dependencies and build vuejs application to `static/dist` folder.

```bash
make prod
make build
```

### 四、其他 

#### 1. 运行方法——2018.06.04
    1) 网页上传csv文件，文件命名方式为“name-学号”
    2) backend/algorithm下执行：
        python run.py first 跑第一个特征
        python run.py second 跑第二个特征

#### 2. 安装步骤—2018.11.20
    1) 安装MinGW，重命名“mingw32-make”为make
    2) 安装anaconda
    3) make dev安装依赖
    4) 安装Python依赖包：

### Be aware

For the sake of simplicity Django config is contained within its own backend app. In real world setting you would
probably want to remove `backend` from `INSTALLED_APPS`, create a new app and move `backend.views` to it.

You probably want to create python virtual environment as well. Default python instance available will be used.
