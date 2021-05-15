from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"Staff"),(3,"Student"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)


class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Staffs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    #fcm_token=models.TextField(default="")
    objects=models.Manager()

class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()



class Subjects(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=255)
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
    staff_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class SessionYearModel(models.Model):
    id=models.AutoField(primary_key=True)
    session_start_year=models.DateField()
    session_end_year=models.DateField()
    object=models.Manager()


class Students(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gender=models.CharField(max_length=255,null=True,blank=True)
    profile_pic=models.FileField(null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    course_id=models.ForeignKey(Courses,on_delete=models.DO_NOTHING,null=True,blank=True)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    phone_number=models.CharField(max_length=255,null=True,blank=True)
    #fcm_token=models.TextField(default="")
    objects = models.Manager()


@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            o=AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            o=Staffs.objects.create(admin=instance)
        if instance.user_type==3:
            #print("here in models.py")
            o=Students(admin=instance)
            #print("2nd last ")
        o.save()
        #print("Last")

class Tests(models.Model):
    test_name=models.CharField(max_length=255,null=True,blank=True)
    conducted_by=models.ForeignKey(Staffs,on_delete=models.CASCADE)
    date=models.DateField()
    #course_id=models.ForeignKey(Courses,on_delete=models.DO_NOTHING,null=True,blank=True)
    subject_id=models.ForeignKey(Subjects,on_delete=models.DO_NOTHING,null=True,blank=True)


########################################################################
#Handle this
class StudentResult(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    marks=models.FloatField(default=0,null=True,blank=True)
    test_id=models.ForeignKey(Tests,default=1,on_delete=models.DO_NOTHING,null=True,blank=True)

    def get_test(self):
        t= Tests.objects.get(id=self.test_id).first()
        return t.test_name
    #subject_id=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    #subject_exam_marks=models.FloatField(default=0)
    #subject_assignment_marks=models.FloatField(default=0)
    #created_at=models.DateField(auto_now_add=True)
    #updated_at=models.DateField(auto_now_add=True)
    #objects=models.Manager()



#Pending
'''
class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Subjects,on_delete=models.DO_NOTHING)
    attendance_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

#Pending
class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

'''

###############################################
#temp
class OnlineClassRoom(models.Model):
    id=models.AutoField(primary_key=True)
    room_name=models.CharField(max_length=255)
    room_pwd=models.CharField(max_length=255)
    subject=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    session_years=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    started_by=models.ForeignKey(Staffs,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    created_on=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
