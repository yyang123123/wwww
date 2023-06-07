from django.contrib import admin
from django.urls import path, include
from .import views

urlpatterns = [
    path('/seoul', views.Seoul),
    path('/busan', views.Busan),
    path('/incheon', views.Incheon),
    path('/daegu', views.Daegu),
    path('/daejeon', views.Daejeon),
    path('/gwangju', views.Gwangju),
    path('/ulsan', views.Ulsan),
    path('/jeju', views.Jeju),

]
