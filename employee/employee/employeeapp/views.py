from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm, RegisterForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render

def index_view(request):
    return render(request, 'index.html')


def register_view(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')

    return render(request, 'register.html', {'form': form})


def login_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('employee_list')

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee_details.html', {'employee': employee})


@login_required
def add_employee(request):
    form = EmployeeForm()

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('employee_list')

    return render(request, 'add_employee.html', {'form': form})


@login_required
def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    form = EmployeeForm(instance=employee)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)

        if form.is_valid():
            form.save()
            return redirect('employee_list')

    return render(request, 'update_employee.html', {'form': form})


@login_required
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')

    return render(request, 'delete_employee.html', {'employee': employee})


@login_required
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully')
            return redirect('employee_list')

    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})