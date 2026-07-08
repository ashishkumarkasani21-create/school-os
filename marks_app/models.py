from django.db import models
from accounts.models import StudentProfile
from academics.models import ExamSchedule

class Mark(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='marks')
    exam_schedule = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'exam_schedule')

    def __str__(self):
        return f"{self.student.user.username} - {self.exam_schedule.subject.name} - {self.marks_obtained}"

    @property
    def percentage(self):
        if self.exam_schedule.max_marks > 0:
            return (self.marks_obtained / self.exam_schedule.max_marks) * 100
        return 0.0

    @property
    def grade(self):
        pct = self.percentage
        if pct >= 90: return 'A+'
        elif pct >= 80: return 'A'
        elif pct >= 70: return 'B'
        elif pct >= 60: return 'C'
        elif pct >= 50: return 'D'
        else: return 'F'
