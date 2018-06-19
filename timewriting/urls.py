from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    path('add_day/', views.add_day, name='add_day'),
    path('your_days/', views.show_days, name='your_days'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]
