from django.db import models
from accounts.models import StudentProfile
from academics.models import Subject

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    )
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendances')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='present')
    remarks = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'date', 'subject')

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name if self.subject else 'General'} - {self.date} - {self.status}"
