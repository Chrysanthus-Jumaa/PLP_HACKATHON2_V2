from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from django.db import transaction


from .models import (
    School, Student, Attendance, User, Teacher, SupportStaff,
    Stream, ClassRoom, FeeRecord, LessonPlan, PlatformConfig,ParentDetails,GuardianDetails
)
from .utils import send_sms

# ----------------------------
# Authentication
# ----------------------------

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        remember = request.POST.get('remember')

        user = authenticate(request, username=username, password=password)

        if user and user.role == role:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)

            # Role-based redirection
            if user.is_superuser or user.is_platform_admin or user.role == 'platform_admin':
                return redirect('platform_dashboard')
            elif user.role == 'admin':
                return redirect('dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user.role == 'parent':
                return redirect('parent_dashboard')
            else:
                return redirect('dashboard')  # fallback

        else:
            return render(request, 'login.html', {'error': 'Invalid credentials or role mismatch'})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# ----------------------------
# Dashboards
# ----------------------------

def get_attendance_percent(school, weekday_name):
    today = timezone.now()
    weekday_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4}
    target_day = weekday_map.get(weekday_name)
    if target_day is None:
        return 0
    target_date = today - timezone.timedelta(days=today.weekday()) + timezone.timedelta(days=target_day)
    records = Attendance.objects.filter(student__school=school, date=target_date)
    total = records.count()
    present = records.filter(status='Present').count()
    return round((present / total) * 100, 2) if total > 0 else 0

@login_required
def dashboard(request):
    user = request.user
    context = {
        'total_students': Student.objects.filter(school=user.school).count(),
        'total_teachers': Teacher.objects.filter(school=user.school).count(),
        'total_staff': SupportStaff.objects.filter(school=user.school).count(),
        'total_streams': Stream.objects.filter(school=user.school).count(),
        'total_classrooms': ClassRoom.objects.filter(school=user.school).count(),
        'boys_count': Student.objects.filter(school=user.school, gender='Male').count(),
        'girls_count': Student.objects.filter(school=user.school, gender='Female').count(),
        'mon_attendance': get_attendance_percent(user.school, 'Monday'),
        'tue_attendance': get_attendance_percent(user.school, 'Tuesday'),
        'wed_attendance': get_attendance_percent(user.school, 'Wednesday'),
        'thu_attendance': get_attendance_percent(user.school, 'Thursday'),
        'fri_attendance': get_attendance_percent(user.school, 'Friday'),
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('dashboard')
    if request.method == 'POST':
        LessonPlan.objects.create(
            teacher=request.user,
            title=request.POST['title'],
            content=request.POST['content']
        )
    plans = LessonPlan.objects.filter(teacher=request.user)
    return render(request, 'teacher_dashboard.html', {'plans': plans})

@login_required
def parent_dashboard(request):
    if request.user.role != 'parent':
        return redirect('dashboard')
    student = Student.objects.filter(parent=request.user).first()
    fee = FeeRecord.objects.filter(student=student).last()
    attendance = Attendance.objects.filter(student=student).order_by('-date')[:10]
    return render(request, 'parent_dashboard.html', {
        'student': student,
        'fee': fee,
        'attendance': attendance
    })

@login_required
def platform_dashboard(request):
    if not request.user.is_platform_admin:
        return redirect('dashboard')

    schools = School.objects.all()
    total_students = Student.objects.count()
    total_teachers = User.objects.filter(role='teacher').count()

    paid = FeeRecord.objects.aggregate(total=Sum('amount_paid'))['total'] or 0
    due = FeeRecord.objects.aggregate(total=Sum('amount_due'))['total'] or 1
    fee_compliance = round((paid / due) * 100, 2)

    school_admins = {
        school.id: school.user_set.filter(role='admin').first()
        for school in schools
    }

    return render(request, 'platform_dashboard.html', {
        'schools': schools,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'fee_compliance': fee_compliance,
        'school_admins': school_admins
    })

# ----------------------------
# School Management
# ----------------------------

@login_required
def register_school(request):
    if not request.user.is_platform_admin:
        return redirect('dashboard')

    if request.method == 'POST':
        school_name = request.POST['school_name']
        address = request.POST['address']
        username = request.POST['admin_username']
        password = request.POST['admin_password']
        confirm = request.POST['confirm_password']

        if password != confirm:
            return render(request, 'register_school.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register_school.html', {'error': 'Username already taken'})

        school = School.objects.create(name=school_name, address=address)
        User.objects.create_user(
            username=username,
            password=password,
            role='admin',
            school=school
        )
        return redirect('platform_dashboard')

    return render(request, 'register_school.html')

@login_required
def view_school(request, school_id):
    school = get_object_or_404(School, id=school_id)
    admin = school.user_set.filter(role='admin').first()
    students = Student.objects.filter(school=school)
    student_count = students.count()

    paid = FeeRecord.objects.filter(student__in=students).aggregate(total=Sum('amount_paid'))['total'] or 0
    due = FeeRecord.objects.filter(student__in=students).aggregate(total=Sum('amount_due'))['total'] or 1
    fee_compliance = round((paid / due) * 100, 2)

    recent_attendance = Attendance.objects.filter(student__in=students).order_by('-date')[:5]

    return render(request, 'view_school.html', {
        'school': school,
        'admin': admin,
        'student_count': student_count,
        'fee_compliance': fee_compliance,
        'recent_attendance': recent_attendance
    })

@login_required
def edit_school(request, school_id):
    if not request.user.is_platform_admin:
        return redirect('dashboard')

    school = get_object_or_404(School, id=school_id)
    admin = school.user_set.filter(role='admin').first()

    if request.method == 'POST':
        school.name = request.POST['school_name']
        school.address = request.POST['address']
        school.save()

        if admin:
            admin.username = request.POST['admin_username']
            password = request.POST['admin_password']
            confirm = request.POST['confirm_password']

            if password and password == confirm:
                admin.set_password(password)
            elif password and password != confirm:
                return render(request, 'edit_school.html', {
                    'school': school,
                    'admin': admin,
                    'error': 'Passwords do not match'
                })

            admin.save()

        return redirect('platform_dashboard')

    return render(request, 'edit_school.html', {
        'school': school,
        'admin': admin
    })

@login_required
def delete_school(request, school_id):
    school = get_object_or_404(School, id=school_id)
    school.delete()
    return redirect('platform_dashboard')

# ----------------------------
# Platform Settings
# ----------------------------

@login_required
def settings_view(request):
    if not request.user.is_platform_admin:
        return redirect('dashboard')

    config, _ = PlatformConfig.objects.get_or_create(id=1)

    if request.method == 'POST':
        config.platform_name = request.POST['platform_name']
        config.admin_email = request.POST['admin_email']
        config.save()
        return render(request, 'settings.html', {
            'platform_name': config.platform_name,
            'admin_email': config.admin_email,
            'success': 'Settings updated successfully!'
        })

    return render(request, 'settings.html', {
        'platform_name': config.platform_name,
        'admin_email': config.admin_email
    })

@login_required
def manage_users_view(request):
    if not request.user.is_platform_admin:
        return redirect('dashboard')

    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

@login_required
def announcements_view(request):
    if not request.user.is_platform_admin:
        return redirect('dashboard')
    return render(request, 'announcements.html')

# ----------------------------
# Student Management
# ----------------------------

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Student, Stream

@login_required
def add_student(request):
    if request.user.role != 'admin':
        return redirect('dashboard')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                stream_name = request.POST.get('stream_name')
                stream, _ = Stream.objects.get_or_create(name=stream_name, school=request.user.school)

                student = Student.objects.create(
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    date_of_birth=request.POST.get('date_of_birth'),
                    gender=request.POST.get('gender'),
                    religion=request.POST.get('religion'),
                    grade=request.POST.get('grade'),
                    passport_photo=request.FILES.get('passport_photo'),
                    school=request.user.school,
                    stream=stream
                )

                if request.POST.get('father_name') or request.POST.get('mother_name'):
                    ParentDetails.objects.create(
                        student=student,
                        father_name=request.POST.get('father_name'),
                        father_phone=request.POST.get('father_phone'),
                        father_occupation=request.POST.get('father_occupation'),
                        mother_name=request.POST.get('mother_name'),
                        mother_phone=request.POST.get('mother_phone'),
                        mother_occupation=request.POST.get('mother_occupation')
                    )
                elif request.POST.get('full_name'):
                    GuardianDetails.objects.create(
                        student=student,
                        full_name=request.POST.get('full_name'),
                        phone=request.POST.get('phone'),
                        occupation=request.POST.get('occupation')
                    )

                return redirect('manage_students')

        except Exception as e:
            return render(request, 'school_admin/add_student.html', {
                'error': f"Failed to register student: {str(e)}"
            })

    return render(request, 'school_admin/add_student.html')

@login_required
def manage_students(request):
    if request.user.role != 'admin':
        return redirect('dashboard')

    students = Student.objects.filter(school=request.user.school).select_related('stream')
    return render(request, 'school_admin/manage_students.html', {'students': students})

# ----------------------------
# Teacher Actions
# ----------------------------

@login_required
def record_attendance(request):
    if request.user.role != 'teacher':
        return redirect('dashboard')

    if request.method == 'POST':
        Attendance.objects.create(
            student_id=request.POST['student_id'],
            date=request.POST['date'],
            status=request.POST['status']
        )
        return redirect('teacher_dashboard')

    students = Student.objects.filter(school=request.user.school)
    return render(request, 'attendance_form.html', {'students': students})

# ----------------------------
# Admin Actions
# ----------------------------

@login_required
def record_fee(request):
    if request.user.role != 'admin':
        return redirect('dashboard')

    if request.method == 'POST':
        student = get_object_or_404(Student, id=request.POST['student_id'])
        FeeRecord.objects.create(
            student=student,
            term=request.POST['term'],
            amount_due=request.POST['amount_due'],
            amount_paid=request.POST['amount_paid']
        )
        notify_parent_fee(student.id)

    return redirect('dashboard')

# ----------------------------
# Utility
# ----------------------------

def notify_parent_fee(student_id):
    student = get_object_or_404(Student, id=student_id)
    parent = student.parent
    fee = FeeRecord.objects.filter(student=student).last()

    if parent and parent.phone_number:
        message = (
            f"Reminder: {student.first_name} {student.last_name}'s fee for {fee.term} "
            f"is KES {fee.amount_due}. Paid: KES {fee.amount_paid}."
        )
        send_sms(parent.phone_number, message)

@login_required
def manage_teachers(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    return render(request, 'school_admin/manage_teachers.html')

@login_required
def add_teacher(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    return render(request, 'school_admin/add_teacher.html')

@login_required
def manage_staff(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    return render(request, 'school_admin/manage_staff.html')

@login_required
def add_staff(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    return render(request, 'school_admin/add_staff.html')

@login_required
def manage_classes(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    return render(request, 'school_admin/manage_classes.html')

@login_required
def add_class(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    return render(request, 'school_admin/add_class.html')

@login_required
def view_student(request, student_id):
    if request.user.role != 'admin':
        return redirect('dashboard')
    student = get_object_or_404(Student, id=student_id, school=request.user.school)
    return render(request, 'school_admin/view_student.html', {'student': student})

@login_required
def edit_student(request, student_id):
    if request.user.role != 'admin':
        return redirect('dashboard')

    student = get_object_or_404(Student, id=student_id, school=request.user.school)
    grades = ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6"]

    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.gender = request.POST.get('gender')
        student.religion = request.POST.get('religion')
        student.grade = request.POST.get('grade')

        stream_name = request.POST.get('stream_name')
        stream, _ = Stream.objects.get_or_create(name=stream_name, school=request.user.school)
        student.stream = stream

        if request.FILES.get('passport_photo'):
            student.passport_photo = request.FILES.get('passport_photo')

        student.save()
        return redirect('manage_students')

    return render(request, 'school_admin/edit_student.html', {
        'student': student,
        'grades': grades
    })

@login_required
def delete_student(request, student_id):
    if request.user.role != 'admin':
        return redirect('dashboard')

    student = get_object_or_404(Student, id=student_id, school=request.user.school)
    stream = student.stream
    student.delete()

    # If no other students are using this stream, delete it
    if not Student.objects.filter(stream=stream).exists():
        stream.delete()

    return redirect('manage_students')
