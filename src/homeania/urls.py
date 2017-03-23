"""homeania URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from accounts.views import (user_login, retake_level, level_complete, practical_test,upload_pic, get_score, save_answer, user_logout, home, ques_list,take_quiz, select_exam)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^exam/(?P<level_id>\d+)$', select_exam, name='select_exam'),
    url(r'^qlist/(?P<level_id>\d+)$', ques_list, name='ques_list'),
    url(r'^test/$', csrf_exempt(save_answer), name='take_quiz'),
    url(r'^score/$', get_score, name='get_score'),
    url(r'^practical-test/(?P<level_id>\d+)$', practical_test, name='practical_test'),
    url(r'^upload/(?P<level_id>\d+)$', upload_pic, name='upload_pic'),    
    url(r'^testing/$', level_complete),
    url(r'^retake/(?P<level_id>\d+)$', retake_level, name='retake_level')
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

