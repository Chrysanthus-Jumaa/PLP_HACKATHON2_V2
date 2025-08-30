from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('platform_admin', 'Platform Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_platform_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Stream(models.Model):
    name = models.CharField(max_length=50)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.school.name}"

class Student(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(default='2000-01-01')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='Male')
    religion = models.CharField(max_length=50, blank=True, default='None')
    grade = models.CharField(max_length=50, default='Grade 1')
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, default=1)
    passport_photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    registration_number = models.CharField(max_length=20, unique=True, editable=False, default='TEMP0000')
    parent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def calculate_age(self):
        return timezone.now().year - self.date_of_birth.year

    def save(self, *args, **kwargs):
        if not self.registration_number or self.registration_number == 'TEMP0000':
            initials = self.first_name[0] + self.last_name[0]
            count = Student.objects.filter(school=self.school).count() + 1
            self.registration_number = f"{initials.upper()}{self.school.id:03d}{count:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ParentDetails(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=100)
    father_phone = models.CharField(max_length=20)
    father_occupation = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mother_phone = models.CharField(max_length=20)
    mother_occupation = models.CharField(max_length=100)

    def __str__(self):
        return f"Parents of {self.student}"

class GuardianDetails(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    occupation = models.CharField(max_length=100)

    def __str__(self):
        return f"Guardian of {self.student}"

class Attendance(models.Model):
    STATUS_CHOICES = [('Present', 'Present'), ('Absent', 'Absent')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"

class FeeRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term = models.CharField(max_length=20)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.term}"

class LessonPlan(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PlatformConfig(models.Model):
    platform_name = models.CharField(max_length=100, default='PlotiYako')
    admin_email = models.EmailField(default='admin@example.com')

    def __str__(self):
        return self.platform_name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SupportStaff(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ClassRoom(models.Model):
    name = models.CharField(max_length=50)
    grade = models.CharField(max_length=20)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - Grade {self.grade}"
