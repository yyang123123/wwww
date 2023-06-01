from django.db import models

# Create your models here.


class Post(models.Model):
    region = models.CharField(max_length=10)
    content = models.TextField()
    sub_content = models.TextField(null=True,blank=True)
    sub_content1 = models.TextField(null=True,blank=True)
    sub_content2 = models.TextField(null=True,blank=True)
    sub_content3 = models.TextField(null=True,blank=True)
    sub_content4 = models.TextField(null=True,blank=True)
    sub_content5 = models.TextField(null=True,blank=True)
    sub_content6 = models.TextField(null=True,blank=True)
    sub_content7 = models.TextField(null=True,blank=True)
    sub_content8 = models.TextField(null=True,blank=True)
    sub_content9 = models.TextField(null=True,blank=True)
