from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_table')
    name=models.CharField(max_length=50)
    referral_user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,name='referral')
    points=models.PositiveIntegerField(blank=True,default=10)