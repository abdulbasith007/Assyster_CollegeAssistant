from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        print(modulename)
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "assyster_app.HodViews":
                    pass
                elif modulename == "assyster_app.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "assyster_app.StaffViews" or modulename == "assyster_app.EditResultVIewClass":
                    pass
                elif modulename == "assyster_app.views" or modulename == "django.views.static":
                    pass
                elif modulename == "assyster_app.OMRViews":
                    pass
                else:
                    #TODO:Verify if staff_home is created
                    return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type == "3":
                if modulename == "assyster_app.StudentViews" or modulename == "django.views.static":
                    pass
                elif modulename == "assyster_app.views":
                    pass
                else:
                    
                    #TODO:Verify if student_home is created
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("loginPage"))

        else:
            if request.path == reverse("loginPage") or modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites" or modulename=="assyster_app.views":
                pass
            else:
                return HttpResponseRedirect(reverse("loginPage"))