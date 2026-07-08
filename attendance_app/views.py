import datetime
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Attendance
from accounts.models import StudentProfile

@login_required
def record_attendance(request):
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, "Unauthorized to record attendance.")
        return redirect('dashboard_redirect')
        
    if request.method == 'POST':
        date_str = request.POST.get('attendance_date')
        if date_str:
            try:
                attendance_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                attendance_date = datetime.date.today()
        else:
            attendance_date = datetime.date.today()
        
        subject_id = request.POST.get('subject_id')
        subject = None
        if subject_id:
            from academics.models import Subject
            subject = Subject.objects.filter(id=subject_id, school=request.user.school).first()

        logged_count = 0
        for key, val in request.POST.items():
            if key.startswith('status_'):
                student_id = key.split('_')[1]
                student = StudentProfile.objects.filter(id=student_id, school=request.user.school).first()
                if student:
                    remarks = request.POST.get(f'remarks_{student_id}', '')
                    Attendance.objects.update_or_create(
                        student=student,
                        date=attendance_date,
                        subject=subject,
                        defaults={'status': val, 'remarks': remarks}
                    )
                    logged_count += 1
                    
        messages.success(request, f"Attendance successfully saved for {logged_count} students on {attendance_date}.")
        
    return redirect('dashboard_redirect')
