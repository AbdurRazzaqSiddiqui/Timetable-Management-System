from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import User, University, Section, Subject, Teacher, Timing, Batch, Timetable_components, Timing, Venue
from django.contrib.auth.models import Group
from .email_verification import compose_email,send_email
from functools import wraps
from django.http import HttpResponseForbidden
from datetime import time

def require_verification():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Check if the attribute is true in the request session
            if request.user.verified:
                # Attribute is true, allow access to the view function
                return view_func(request, *args, **kwargs)
            else:
                # Attribute is not true, return forbidden response
                return render(request, 'TMS/verify_email.html',{
                    'user_email':request.session['email']
                }
                )
        return wrapper
    return decorator

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('TMS:index'))
    if request.method == 'POST':
        request.session['username'] = request.POST['username']
        request.session['password'] = request.POST['password']
        user = authenticate(request, username=request.session['username'], password=request.session['password'])
        if user is not None:
            login(request,user)
            if not User.objects.get(username=request.session['username']).verified:
                return render(request, 'TMS/verify_email.html',{
                    'user_email':User.objects.get(username=request.session['username']).email
                }
                )
            return HttpResponseRedirect(reverse('TMS:index'))
        else:
            print("Invalid Username or Password")
            return render(request, 'TMS/form.html')
    else:
        return render(request, 'TMS/form.html')

def register_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('TMS:index'))
    if request.method == 'POST':
        request.session['username'] = request.POST['username']
        if University.objects.get(university_name='FAST NUCES').university_email in request.POST['email']:
            request.session['email'] = request.POST['email']
        else:
            print("Please Enter your University Email Address.")
            return render(request, 'TMS/form.html')
        request.session['password'] = request.POST['password']
        request.session['confirmation'] = request.POST['confirmation']
        if request.POST['password'] == request.POST['confirmation'] and not (User.objects.filter(email=request.POST['email']).exists()) and not (User.objects.filter(username=request.POST['username']).exists()):
            verification_code = compose_email(request.session['username'],request.session['email'])
            user = User.objects.create_user(request.session['username'],request.session['email'],request.session['password'],is_active=True,is_staff=False, verification_code=verification_code)
            user.save()
            login(request,user)
            if request.POST['user'] == 'student':
                group = Group.objects.get(name='Students')
            elif request.POST['user'] == 'teacher':
                group = Group.objects.get(name='Teachers')
            group.user_set.add(user)
            return render(request, 'TMS/verify_email.html',{
                'user_email':request.session['email']
            })
        else:
            print("Username or Email already taken.")
            return render(request, 'TMS/form.html')
    else:
        return render(request, 'TMS/form.html')

# def verify_first(request):
#     request.session['staff'] = User.objects.get(username=request.user.username).verified
#     print(request.session['staff'])
#     if not bool(request.session['staff']):
#         print("Hello")
#         request.session['email'] = User.objects.get(username=request.user.username).email
#         return False
#     else:
#         return True

@login_required(login_url='TMS:login')
@require_verification()
def index(request):
    # if not verify_first(request):
    #     return render(request, 'TMS/verify_email.html',{
    #         'user_email':request.session['email']
    #     }
    #     )
    # else:
    # Create_Timetable_Components()
    # Timings_and_Venues()
    # print(Timetable_components.objects.all())
    Generate_Timetable()
    Generate_Excel_Sheet()
    return HttpResponse("hello world!")

def verify_email(request):
    user = request.user
    request.session['email'] = User.objects.get(username=user.username).email
    if request.method == 'POST':
        print(user.verification_code)
        print(request.POST['verification_code'])
        if int(request.POST['verification_code']) == int(user.verification_code):
            user.verified == True
            user.save()
            return HttpResponseRedirect(reverse('TMS:index'))
    else:
        return render(request, 'TMS/verify_email.html',{
            'user_email':request.session['email']
        }
        )

def Create_Timetable_Components():
    batches = Batch.objects.all()
    for batch in batches:
        sections = Section.objects.filter(batch=batch)
        subjects = Subject.objects.get(batch=batch).subjects_1
        for section in sections:
            for subject in subjects:
                teacher = Teacher.objects.create(teacher_name="Sample")
                teacher.save()
                teacher.subjects.add(Subject.objects.get(batch=batch.pk))
                teacher.save()
                # for i in range(3):
                comp = Timetable_components.objects.create(section=section,subject=subject,teacher=teacher)
                # print(comp)

def Timings_and_Venues():
    for i in range(1,21):
        Venue.objects.create(venue_code=f"E{i}",capacity=50)

    days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    for i in range(1):
        for j in range(8):
            s_time = time(j+8,0)
            e_time = time(j+8,55)
            Timing.objects.create(day_of_week=days[i],start_time=s_time,end_time=e_time)

def Create_Table():
    timetable = []
    for _ in range(len(Venue.objects.all())):
        timetable.append([])

    for i in range(len(Venue.objects.all())):
        for _ in range(len(Timing.objects.all())):
            timetable[i].append(0)


    return timetable

def Check_Conflict(table, j, obj):
    for i in range(len(table)):
        if table[i][j] != 0:
            if obj.section == table[i][j].section or obj.teacher == table[i][j].teacher:
                return False

    return True

def Generate_Timetable():
    table = Create_Table()
    timetable_objects = Timetable_components.objects.all()
    flag = False
    for obj in timetable_objects:
        for i in range(len(table)):
            for j in range(len(table[i])):
                if(Check_Conflict(table,j,obj) and table[i][j] == 0):
                    table[i][j] = obj
                    flag = True
                    break
            if(flag):
                flag = False
                break

    for j in range(len(Timing.objects.all())):
        for i in range(len(Venue.objects.all())):
            if table[i][j] == 0: 
                print("None")
            else:
                print(f"{table[i][j].section}, {table[i][j].subject}")
        print()

from openpyxl import Workbook

def Generate_Excel_Sheet():
    wb = Workbook()
    ws = wb.active

    venues = Venue.objects.all()
    for i, venue in enumerate(venues, start=2):
        venue_name = f"{venue.venue_code}"
        tuple_name = f'A{i}'
        ws[tuple_name] = venue_name

    timings = Timing.objects.all()
    for i, timing in enumerate(timings, start=2):
        timing_name = f"{timing.start_time} - {timing.end_time}"
        tuple_name = f'{chr(64 + i)}1'
        ws[tuple_name] = timing_name

    wb.save('example.xlsx')

