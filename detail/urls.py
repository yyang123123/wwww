from django.urls import path, include
from .import views


urlpatterns = [
    path('gyeong', views.gyeong),
    path('Namsan', views.Namsan),
    path('Dongdaemun', views.Dongdaemun),
    path('Lotte', views.Lotte),
    path('myeongdongseongdang', views.myeongdongseongdang),
    path('seoulgwangjang', views.seoulgwangjang),
    path('sebichseom', views.sebichseom),
    path('changdeoggung', views.changdeoggung),
]
