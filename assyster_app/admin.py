from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Courses)
admin.site.register(models.Students)
admin.site.register(models.Staffs)
admin.site.register(models.Subjects)
admin.site.register(models.StudentResult)
admin.site.register(models.Tests)