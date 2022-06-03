"""mySpartaSns URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from . import views     # 현재 폴더에서 views 파일 가져온다.


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.base_response, name='first_test'),  # test/ url로 views파일의 base_response 함수와 연결 시켜줌
    path('first/', views.first_view, name='first_view'),
    path('',include('user.urls')),  # user의 url과 mySparta의 url 을 연결해줌
    path('',include('tweet.urls')), # user.urls 는 일치하는 url이 없고 tweet.urls가 응답
]
