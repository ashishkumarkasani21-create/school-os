from django.contrib.auth.models import AbstractUser
from django.db import models
from schools.models import School

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('principal', 'Principal'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('accountant', 'Accountant'),
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class PrincipalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'principal'}, related_name='principal_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Principal: {self.user.get_full_name() or self.user.username}"

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='teacher_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=100, default='Class Teacher')
    qualification = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Teacher: {self.user.get_full_name() or self.user.username}"

class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'parent'}, related_name='parent_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Parent: {self.user.get_full_name() or self.user.username}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='student_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50, blank=True, null=True)
    class_room = models.ForeignKey('academics.ClassRoom', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    roll_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    parent = models.ForeignKey(ParentProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return f"Student: {self.user.get_full_name() or self.user.username}"

class AccountantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'accountant'}, related_name='accountant_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Accountant: {self.user.get_full_name() or self.user.username}"
