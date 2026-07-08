from django.db import models
from academics.models import ClassRoom, Subject
from accounts.models import TeacherProfile, StudentProfile

class Homework(models.Model):
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='homeworks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    date_assigned = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    attachment = models.FileField(upload_to='homework_attachments/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.class_room}"

class HomeworkSubmission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='homework_submissions')
    date_submitted = models.DateTimeField(auto_now_add=True)
    text_response = models.TextField(blank=True, null=True)
    file_submission = models.FileField(upload_to='homework_submissions/', blank=True, null=True)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('homework', 'student')

    def __str__(self):
        return f"{self.student.user.username} - {self.homework.title}"
