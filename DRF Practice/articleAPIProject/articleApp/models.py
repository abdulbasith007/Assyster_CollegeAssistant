from django.db import models

# Create your models here.

class Articles(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    #profile_pic=models.FileField(null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    #course_id=models.ForeignKey(Courses,on_delete=models.DO_NOTHING,null=True,blank=True)
    #session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE,null=True,blank=True)
    #created_at=models.DateTimeField(auto_now_add=True)
    #updated_at=models.DateTimeField(auto_now_add=True)
    #fcm_token=models.TextField(default="")
    #objects = models.Manager()