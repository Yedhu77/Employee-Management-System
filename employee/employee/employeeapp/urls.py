from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index_view, name='index'),

    path('employees/', views.employee_list, name='employee_list'),

    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),

    path('add/', views.add_employee, name='add_employee'),

    path('update/<int:pk>/', views.update_employee, name='update_employee'),

    path('delete/<int:pk>/', views.delete_employee, name='delete_employee'),

    path('register/', views.register_view, name='register'),

    path('', views.login_view, name='login'),

    path('logout', views.logout_view, name='logout'),

    path('change-password/', views.change_password, name='change_password'),
]