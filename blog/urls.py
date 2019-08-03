"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include, re_path
from app001 import views
from django.views.static import serve
from django.conf import settings
from app001 import urls as blog_urls
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/', views.reg),
    path('index/', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('upload/', views.upload),
    # 交给app0001的url 处理
    re_path(r'^blog', include(blog_urls)),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

]


