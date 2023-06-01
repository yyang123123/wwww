from django.urls import path, include
from .import views


urlpatterns = [
    path('gyeong', views.gyeong),
    path('namsan', views.Namsan),
]
