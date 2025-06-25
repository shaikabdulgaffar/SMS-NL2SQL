from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student, Department
from .forms import StudentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count, Q

@login_required
def student_list(request):
    from .models import Student, Department
    total_students = Student.objects.count()
    total_departments = Department.objects.count()
    dept_id = request.GET.get('dept')
    if dept_id:
        department = get_object_or_404(Department, pk=dept_id)
        students = Student.objects.filter(present_department=department.name)
        return render(request, 'students/student_list.html', {
            'students': students,
            'department': department,
            'departments': Department.objects.all(),
            'total_students': total_students,
            'total_departments': total_departments,
        })
    else:
        departments = Department.objects.all()
        dept_counts = []
        for dept in departments:
            count = Student.objects.filter(present_department=dept.name).count()
            dept_counts.append({'dept': dept, 'student_count': count})
        return render(request, 'students/student_list.html', {
            'departments': dept_counts,
            'students': None,
            'total_students': total_students,
            'total_departments': total_departments,
        })

@login_required
def student_add(request):
    dept_id = request.GET.get('dept')
    initial = {}
    if dept_id:
        from .models import Department
        try:
            dept = Department.objects.get(pk=dept_id)
            initial['present_department'] = dept
        except Department.DoesNotExist:
            pass
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(initial=initial)
    return render(request, 'students/student_form.html', {'form': form})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('student_list')

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'students/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_departments = Department.objects.count()
    day_scholars = Student.objects.filter(scholar_type='dayscholar').count()
    hostelers = Student.objects.filter(scholar_type='hosteler').count()
    # Gender fields ab nahi hain, isliye boys/girls ko 0 set kar dein ya hata dein
    boys = 0
    girls = 0
    return render(request, 'dashboard.html', {
        'total_students': total_students,
        'total_departments': total_departments,
        'day_scholars': day_scholars,
        'hostelers': hostelers,
        'boys': boys,
        'girls': girls,
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Session logout na ho
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})