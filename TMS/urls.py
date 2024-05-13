from django.urls import path
from . import views

app_name = 'TMS'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('verify', views.verify_email, name='verify_email'),
    path('university_details', views.University_Form, name='university_info_form'),
    path('semester_details', views.Semester_Form, name='semester_info_form'),
    path('teacher_timetable', views.teacher_timetable, name='teacher_timetable')
]
