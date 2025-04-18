from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('predict/', views.predict_status, name='predict'),
    path('visualisation/', views.visualisation, name='visualisation'),
]
