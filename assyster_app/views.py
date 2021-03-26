from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect

from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from assyster_app.EmailBackEnd import EmailBackEnd

from django.urls import reverse
from .models import CustomUser,Students,Staffs,Courses,SessionYearModel,Subjects
# Create your views here.



def ShowLoginPage(request):
    if request.method!="POST":
        return render(request,"assyster_app/login_page.html")
    else:
        
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                #return HttpResponse('admin/')
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                #return HttpResponse('admin/')
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                #return HttpResponse('admin/')
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")



def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

#I think signup as an admin shouldnt be allowed,bcz anyone can access in this case
'''
def signup_admin(request):
    return render(request,"signup_admin_page.html")
'''

def signup_student(request):
    if request.method!="POST":
        courses=Courses.objects.all()
        session_years=SessionYearModel.object.all()
        return render(request,"assyster_app/signup_student_page.html",{"courses":courses,"session_years":session_years})
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        session_year_id = request.POST.get("session_year")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")

        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        #try:
        user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name,
                                            first_name=first_name, user_type=3)
        user.students.address = address
        course_obj = Courses.objects.get(id=course_id)
        user.students.course_id = course_obj
        session_year = SessionYearModel.object.get(id=session_year_id)
        user.students.session_year_id = session_year
        user.students.gender = sex
        user.students.profile_pic = profile_pic_url
        user.students.save()
        user.save()
        messages.success(request, "Successfully Added Student")
        return HttpResponseRedirect(reverse("loginPage"))
        #except:
        #   messages.error(request, "Failed to Add Student")
        #  return HttpResponseRedirect(reverse("loginPage"))

def signup_staff(request):
    if request.method!="POST":
        return render(request,"assyster_app/signup_staff_page.html")
    else:
        
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
            user.staffs.address=address
            user.staffs.save()
            user.save()
            messages.success(request,"Successfully Created Staff")
            return HttpResponseRedirect(reverse("loginPage"))
        except:
            messages.error(request,"Failed to Create Staff")
            return HttpResponseRedirect(reverse("loginPage"))
