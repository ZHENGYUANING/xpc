"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web.views import post, composer

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^show_list/$', post.show_list),
    url(r'^show_list/(?P<page>\d+)/$', post.show_list),
    url(r'^user/oneuser/userid-(?P<cid>\d+)$', composer.oneuser),
    url(r'^u(?P<cid>\d+)$', composer.homepage),
    url(r'^a(?P<pid>\d+)$', post.detail),
    url(r'^article/filmplay/ts-getCommentApi$', post.comments),
    url(r'^register$', composer.register),  # 显示注册页面
    url(r'^api/v1/mobile/send$', composer.send_code),  # 发送手机验证码
    url(r'^api/v1/user/register$', composer.do_register),  # 执行注册操作
    url(r'^login/$', composer.login),  # 显示登录页面
    url(r'^api/v1/user/login$', composer.do_login),  # 执行登录操作
]
from django.conf import settings
if settings.DEBUG:
    from django.conf.urls import include, url
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns