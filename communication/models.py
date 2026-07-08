from django.db import models
from django.conf import settings
from schools.models import School

class Announcement(models.Model):
    ROLE_TARGETS = (
        ('all', 'All Roles'),
        ('principal', 'Principal Only'),
        ('teacher', 'Teachers Only'),
        ('student', 'Students Only'),
        ('parent', 'Parents Only'),
        ('accountant', 'Accountants Only'),
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    target_role = models.CharField(max_length=20, choices=ROLE_TARGETS, default='all')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Complaint(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    resolution_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
