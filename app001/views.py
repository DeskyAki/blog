from django.shortcuts import render, redirect, HttpResponse
from app001 import form
from app001 import models
from django.contrib import auth
from django.http import JsonResponse
from bs4 import BeautifulSoup
from django.db.models import F
from blog import settings
import os
import json


def reg(request):
    if request.method == "POST":
        form_obj = form.RegForm(request.POST)
        if form_obj.is_valid():
            form_obj.cleaned_data.pop("re_password")
            avatar_img = request.FILES.get("avatar")
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            return redirect("/index/")
        else:
            return render(request, "reg.html", {"form_obj": form_obj})
    form_obj = form.RegForm()
    return render(request, "reg.html", {"form_obj": form_obj})


def index(request):
    article_list = models.Article.objects.all()
    return render(request, "index.html", {"article_list": article_list})


def login(request):
    if request.method == "POST":
        msg = {"username": "", "password": ""}
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect("/index/")
        else:
            if models.UserInfo.objects.filter(username=username):
                msg["password"] = "密码错误"
            else:
                msg["username"] = "查无此人"
            return JsonResponse(msg)
            # return render(request, "login.html", {"msg": msg})
    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("/index/")


def home(request, username):
    user = models.UserInfo.objects.filter(username=username).first()  # username是userinfo继承的AbstractUser 中的字段
    # .first 很重要 没有就报错 说没有属性
    if not user:
        return render(request, '404.html')
    blog = user.blog
    article_list = models.Article.objects.filter(user=user)
    return render(request, "home.html", {"blog": blog, "username": username, "article_list": article_list})


def article_detail(request, username, pk):
    user = models.UserInfo.objects.filter(username=username).first()
    comment_list = models.Comment.objects.filter(article_id=pk)
    if not user:
        return render(request, '404.html')
    blog = user.blog
    article_obj = models.Article.objects.filter(pk=pk).first()
    return render(request, "article_detail.html", {"username": username, "article": article_obj, "blog": blog,
                                                   "comment_list": comment_list})


def up_down(request):
    article_id = request.POST.get("article_id")
    is_up = json.loads(request.POST.get("is_up"))  # 转为能认识python格式 json是小true python是RUE
    response = {"state": True}
    user = request.user
    try:
        if is_up:
            models.ArticleUpDown.objects.create(user=user, article_id=article_id, is_up=is_up)
            models.Article.objects.filter(pk=article_id).update(up_count=F("up_count")+1)

        else:
            models.ArticleUpDown.objects.create(user=user, article_id=article_id, is_up=is_up)
            models.Article.objects.filter(pk=article_id).update(down_count=F("down_count")+1)

    except Exception as e:
        # 报错说明user=user, article_id=article_id 已经存在 因为她们两个联合为一
        response["state"] = False
        response["first_action"] = models.ArticleUpDown.objects.filter(user=user, article_id=article_id).first().is_up

    return JsonResponse(response)


def comment(request):
    pid = request.POST.get("pid")
    article_id = request.POST.get("article_id")
    content = request.POST.get("content")
    user_pk = request.user.pk
    response = {}
    if not pid:
        comment_obj = models.Comment.objects.create(article_id=article_id, user_id=user_pk, content=content)
    else:
        comment_obj = models.Comment.objects.create(article_id=article_id, user_id=user_pk, content=content,
                                                    parent_comment_id=pid)
    response["create_time"] = comment_obj.create_time
    # . strftime("%Y-%m-%d")  加不加呢
    response["content"] = comment_obj.content
    response["username"] = comment_obj.user.username
    return JsonResponse(response)


def comment_tree(request, article_id):
    ret = list(models.Comment.objects.filter(article_id=article_id).values("pk", "content", "parent_comment_id"))
    return JsonResponse(ret, safe=False)


def add_article(request):
    if request.method == "POST":

        title = request.POST.get("title")
        article_content = request.POST.get("article_content")
        user = request.user
        bs = BeautifulSoup(article_content, "html.parser")
        desc = bs.text[0:200] + "..."
        # 过滤 非法标签
        for tag in bs.find_all():
            if tag.name in ["script", "link"]:
                tag.decompose()
        article_obj = models.Article.objects.create(user=user, title=title, desc=desc)
        models.ArticleDetail.objects.create(content=str(bs), article=article_obj)
        return redirect("/blog/"+request.user.username+"/")
    return render(request, "add_article.html")


def upload(request):
    obj = request.FILES.get("upload_img")
    path = os.path.join(settings.MEDIA_ROOT, "add_article_img", obj.name)
    # obj.name 文件的名字
    with open(path, "wb") as f:
        for i in obj:
            f.write(i)
    res = {
        # 必须返回数字
        "error": 0,
        "url": "/media/add_article_img/" + obj.name
    }
    return JsonResponse(res)

