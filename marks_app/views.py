from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Mark
from academics.models import ExamSchedule
from accounts.models import StudentProfile

@login_required
def record_marks(request):
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, "Unauthorized to record marks.")
        return redirect('dashboard_redirect')
        
    if request.method == 'POST':
        schedule_id = request.POST.get('exam_schedule_id')
        exam_schedule = get_object_or_404(ExamSchedule, id=schedule_id)
        
        logged_count = 0
        for key, val in request.POST.items():
            if key.startswith('marks_'):
                student_id = key.split('_')[1]
                student = StudentProfile.objects.filter(id=student_id, school=request.user.school).first()
                if student and val != '':
                    try:
                        obtained = float(val)
                        if obtained > exam_schedule.max_marks:
                            obtained = exam_schedule.max_marks
                        
                        remarks = request.POST.get(f'remarks_{student_id}', '')
                        Mark.objects.update_or_create(
                            student=student,
                            exam_schedule=exam_schedule,
                            defaults={'marks_obtained': obtained, 'remarks': remarks}
                        )
                        logged_count += 1
                    except ValueError:
                        pass
                        
        messages.success(request, f"Marks entry completed for {logged_count} students in {exam_schedule.subject.name}.")
        
    return redirect('dashboard_redirect')
