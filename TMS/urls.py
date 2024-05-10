from django.urls import path
from . import views

app_name = 'TMS'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('verify', views.verify_email, name='verify_email'),
]
