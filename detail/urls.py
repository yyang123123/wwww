from django.urls import path, include
from .import views


urlpatterns = [
    path('gyeong', views.gyeong),
    path('changdeok', views.changdeok),
    path('dongdaemoon', views.dongdaemoon),
    path('hangang', views.hangang),
    path('lotte', views.lotte),
    path('namsan', views.namsan),
    path('seoulchurch', views.seoulchurch),
    path('seoulpark', views.seoulpark),
]
