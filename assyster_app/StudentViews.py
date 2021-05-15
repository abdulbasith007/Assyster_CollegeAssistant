
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from assyster_app.models import CustomUser, Staffs, Courses, Subjects, Students, SessionYearModel,OnlineClassRoom,StudentResult,Tests#, \
    #FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport, \
    #NotificationStudent, NotificationStaffs


from django.contrib import messages
def student_home(request):
    student_obj=Students.objects.get(admin=request.user.id)
    #attendance_total=AttendanceReport.objects.filter(student_id=student_obj).count()
    #attendance_present=AttendanceReport.objects.filter(student_id=student_obj,status=True).count()
    #attendance_absent=AttendanceReport.objects.filter(student_id=student_obj,status=False).count()
    course=Courses.objects.get(id=student_obj.course_id.id)
    subjects=Subjects.objects.filter(course_id=course).count()
    subjects_data=Subjects.objects.filter(course_id=course)
    session_obj=SessionYearModel.object.get(id=student_obj.session_year_id.id)
    class_room=OnlineClassRoom.objects.filter(subject__in=subjects_data,is_active=True,session_years=session_obj)

    subject_name=[]
    data_present=[]
    data_absent=[]
    subject_data=Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        #attendance=Attendance.objects.filter(subject_id=subject.id)
        #attendance_present_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=True,student_id=student_obj.id).count()
        #attendance_absent_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=False,student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        #data_present.append(attendance_present_count)
        #data_absent.append(attendance_absent_count)
        print(request.user.students)
    results=StudentResult.objects.filter(student_id=request.user.students)
    print("##################################")
    Results=[]
    for r in results:
        print(r.marks)
        #t=Tests.objects.filter(pk=r.test_id).first()
        t=Tests.objects.get(id=r.test_id.id)
        print(t.test_name)
        Results.append([r.marks,t.test_name])
        #print(r.get_test())
    print(Results)
    return render(request,"assyster_app/student_template/student_home_template.html",{"total_attendance":10,"attendance_absent":2,"attendance_present":8,"subjects":subjects,"data_name":subject_name,"data1":data_present,"data2":data_absent,"class_room":class_room,"results":Results})

    #"total_attendance":attendance_total,"attendance_absent":attendance_absent,"attendance_present":attendance_present,"class_room":class_room


def join_class_room(request,subject_id,session_year_id):
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    subjects=Subjects.objects.filter(id=subject_id)
    if subjects.exists():
        session=SessionYearModel.object.filter(id=session_year_obj.id)
        if session.exists():
            subject_obj=Subjects.objects.get(id=subject_id)
            course=Courses.objects.get(id=subject_obj.course_id.id)
            check_course=Students.objects.filter(admin=request.user.id,course_id=course.id)
            if check_course.exists():
                session_check=Students.objects.filter(admin=request.user.id,session_year_id=session_year_obj.id)
                if session_check.exists():
                    onlineclass=OnlineClassRoom.objects.get(session_years=session_year_id,subject=subject_id)
                    return render(request,"assyster_app/student_template/join_class_room_start.html",{"username":request.user.username,"password":onlineclass.room_pwd,"roomid":onlineclass.room_name})

                else:
                    return HttpResponse("This Online Session is Not For You")
            else:
                return HttpResponse("This Subject is Not For You")
        else:
            return HttpResponse("Session Year Not Found")
    else:
        return HttpResponse("Subject Not Found")


