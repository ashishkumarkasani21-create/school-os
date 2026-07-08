from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Homework, HomeworkSubmission
from academics.models import ClassRoom, Subject
from accounts.models import StudentProfile
import datetime

@login_required
def create_homework(request):
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, "Unauthorized to assign homework.")
        return redirect('dashboard_redirect')
        
    if request.method == 'POST':
        class_room_id = request.POST.get('class_room_id')
        subject_id = request.POST.get('subject_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_str = request.POST.get('due_date')
        attachment = request.FILES.get('attachment')

        classroom = get_object_or_404(ClassRoom, id=class_room_id, school=request.user.school)
        subject = get_object_or_404(Subject, id=subject_id, school=request.user.school)
        
        try:
            due_date = datetime.datetime.strptime(due_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            due_date = datetime.date.today() + datetime.timedelta(days=2)

        Homework.objects.create(
            class_room=classroom,
            subject=subject,
            teacher=request.user.teacher_profile,
            title=title,
            description=description,
            due_date=due_date,
            attachment=attachment
        )
        messages.success(request, f"New homework assignment '{title}' posted successfully.")
        
    return redirect('dashboard_redirect')

@login_required
def submit_homework(request):
    if request.user.role != 'student':
        messages.error(request, "Only students can submit homework.")
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        hw_id = request.POST.get('homework_id')
        text_resp = request.POST.get('text_response')
        file_sub = request.FILES.get('file_submission')
        
        homework = get_object_or_404(Homework, id=hw_id, class_room=request.user.student_profile.class_room)

        HomeworkSubmission.objects.update_or_create(
            homework=homework,
            student=request.user.student_profile,
            defaults={
                'text_response': text_resp,
                'file_submission': file_sub,
                'date_submitted': datetime.datetime.now()
            }
        )
        messages.success(request, f"Homework submission for '{homework.title}' saved successfully.")

    return redirect('dashboard_redirect')
