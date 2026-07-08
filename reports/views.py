from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.db.models import Sum, Avg, Count

from schools.models import School
from accounts.models import (
    User, PrincipalProfile, TeacherProfile, StudentProfile, ParentProfile, AccountantProfile
)
from academics.models import ClassRoom, Subject, ClassSubject, Timetable, Exam, ExamSchedule
from attendance_app.models import Attendance
from homework_app.models import Homework, HomeworkSubmission
from marks_app.models import Mark
from finance.models import FeeStructure, StudentFee, Payment, Receipt, Concession
from transport.models import Bus, Route, Stop, StudentBusAssignment, BusLocationLog
from ocr_app.models import OCRDocument, OCRExtractionResult
from communication.models import Announcement, Complaint
from leave_app.models import LeaveRequest
from school_os.helpers import school_has_feature

# Dashboard Access Decorator
def role_required(allowed_roles):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in allowed_roles:
                return HttpResponseForbidden("You do not have permission to view this page.")
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator

@login_required
@role_required(['admin'])
def admin_dashboard(request):
    school = request.user.school
    if not school:
        return render(request, 'reports/no_school.html')

    # Handle Announcement Creation
    if request.method == 'POST' and 'announce_title' in request.POST:
        title = request.POST.get('announce_title')
        content = request.POST.get('announce_content')
        target = request.POST.get('announce_target', 'all')
        Announcement.objects.create(
            school=school,
            title=title,
            content=content,
            created_by=request.user,
            target_role=target
        )
        messages.success(request, f"Announcement '{title}' broadcast successfully.")
        return redirect('admin_dashboard')

    # Handle Class Creation
    if request.method == 'POST' and 'create_class_name' in request.POST:
        name = request.POST.get('create_class_name').strip()
        section = request.POST.get('create_class_section').strip().upper()
        if ClassRoom.objects.filter(school=school, name=name, section=section).exists():
            messages.error(request, f"Class '{name} - {section}' already exists.")
        else:
            ClassRoom.objects.create(school=school, name=name, section=section)
            messages.success(request, f"Class '{name} - {section}' successfully created.")
        return redirect('admin_dashboard')

    # Handle Class Teacher Assignment
    if request.method == 'POST' and 'assign_class_id' in request.POST:
        class_id = request.POST.get('assign_class_id')
        teacher_id = request.POST.get('assign_teacher_id')
        classroom = ClassRoom.objects.filter(id=class_id, school=school).first()
        
        # Parse teacher (allow None for unassigning)
        teacher = None
        if teacher_id:
            teacher = TeacherProfile.objects.filter(id=teacher_id, school=school).first()

        if classroom:
            classroom.class_teacher = teacher
            classroom.save()
            if teacher:
                messages.success(request, f"Assigned {teacher.user.get_full_name() or teacher.user.username} as Class Teacher for {classroom.name} - {classroom.section}.")
            else:
                messages.success(request, f"Successfully unassigned Class Teacher from {classroom.name} - {classroom.section}.")
        return redirect('admin_dashboard')

    # Handle User Creation
    if request.method == 'POST' and 'create_username' in request.POST:
        uname = request.POST.get('create_username').strip().lower()
        pwd = request.POST.get('create_password')
        role = request.POST.get('create_role')
        name = request.POST.get('create_name', '')
        
        # Split name
        first_name = name
        last_name = ''
        if ' ' in name:
            first_name, last_name = name.split(' ', 1)
            
        if User.objects.filter(username=uname).exists():
            messages.error(request, f"Username/ID '{uname}' already exists. Please select a unique identifier.")
        else:
            new_user = User.objects.create_user(
                username=uname,
                password=pwd,
                role=role,
                school=school,
                first_name=first_name,
                last_name=last_name,
                email=f"{uname}@{school.code}.edu"
            )
            # Create corresponding profile
            if role == 'student':
                class_id = request.POST.get('student_class')
                classroom = ClassRoom.objects.filter(id=class_id, school=school).first() if class_id else None
                StudentProfile.objects.create(
                    user=new_user,
                    school=school,
                    student_id=f"STU-{new_user.id:04d}",
                    class_room=classroom,
                    roll_number=str(100 + new_user.id)
                )
            elif role == 'teacher':
                TeacherProfile.objects.create(
                    user=new_user,
                    school=school,
                    employee_id=f"TCH-{new_user.id:04d}"
                )
            elif role == 'accountant':
                AccountantProfile.objects.create(
                    user=new_user,
                    school=school,
                    employee_id=f"ACC-{new_user.id:04d}"
                )
            elif role == 'principal':
                PrincipalProfile.objects.create(
                    user=new_user,
                    school=school
                )
            messages.success(request, f"User account '{uname}' successfully registered as {role.capitalize()}.")
        return redirect('admin_dashboard')

    # Quick statistics
    total_students = StudentProfile.objects.filter(school=school).count()
    total_teachers = TeacherProfile.objects.filter(school=school).count()
    total_accountants = AccountantProfile.objects.filter(school=school).count()
    active_buses = Bus.objects.filter(school=school, status='active').count()

    # User lists
    students = StudentProfile.objects.filter(school=school).select_related('user', 'class_room')
    teachers = TeacherProfile.objects.filter(school=school).select_related('user')
    accountants = AccountantProfile.objects.filter(school=school).select_related('user')
    classes = ClassRoom.objects.filter(school=school)

    # Announcements
    announcements = Announcement.objects.filter(school=school).order_by('-created_at')[:5]


    context = {
        'school': school,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_accountants': total_accountants,
        'active_buses': active_buses,
        'students': students,
        'teachers': teachers,
        'accountants': accountants,
        'classes': classes,
        'announcements': announcements,
    }
    return render(request, 'reports/admin_dashboard.html', context)

@login_required
@role_required(['principal'])
def principal_dashboard(request):
    school = request.user.school
    
    # Feature gate check: requires Gold or Platinum
    has_access = school_has_feature(school, 'accounting_reports') # Key Gold feature
    if not has_access:
        return render(request, 'reports/upgrade_prompt.html', {'plan_required': 'Gold'})

    # Principal Analytics
    total_students = StudentProfile.objects.filter(school=school).count()
    total_teachers = TeacherProfile.objects.filter(school=school).count()
    
    # Average attendance
    today = timezone.localdate()
    attendance_today = Attendance.objects.filter(student__school=school, date=today)
    total_att = attendance_today.count()
    present_att = attendance_today.filter(status='present').count()
    attendance_rate = (present_att / total_att * 100) if total_att > 0 else 92.5  # Realistic mock default

    # Financial collection summary
    total_receivable = StudentFee.objects.filter(student__school=school).aggregate(sum=Sum('amount'))['sum'] or 0
    total_collected = StudentFee.objects.filter(student__school=school).aggregate(sum=Sum('paid_amount'))['sum'] or 0
    total_dues = total_receivable - total_collected

    # Leave requests
    pending_leaves = LeaveRequest.objects.filter(user__school=school, status='pending')

    # OCR documents pending review
    pending_ocr = OCRDocument.objects.filter(school=school, status='pending')

    # Complaints
    complaints = Complaint.objects.filter(school=school).order_by('-created_at')[:5]

    # Announcements
    announcements = Announcement.objects.filter(school=school, target_role__in=['all', 'principal']).order_by('-created_at')[:5]

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'attendance_rate': round(attendance_rate, 1),
        'total_receivable': total_receivable,
        'total_collected': total_collected,
        'total_dues': total_dues,
        'pending_leaves': pending_leaves,
        'pending_ocr': pending_ocr,
        'complaints': complaints,
        'announcements': announcements,
    }
    return render(request, 'reports/principal_dashboard.html', context)

@login_required
@role_required(['accountant'])
def accountant_dashboard(request):
    school = request.user.school
    
    # Feature gate check: requires Gold or Platinum
    has_access = school_has_feature(school, 'accounting_reports')
    if not has_access:
        return render(request, 'reports/upgrade_prompt.html', {'plan_required': 'Gold'})

    # Accountant stats
    total_due = StudentFee.objects.filter(student__school=school).exclude(status='paid')
    total_due_amount = sum(fee.balance for fee in total_due)

    payments_today = Payment.objects.filter(
        student_fee__student__school=school, 
        payment_date__date=timezone.localdate()
    ).aggregate(sum=Sum('amount_paid'))['sum'] or 0

    recent_payments = Payment.objects.filter(student_fee__student__school=school).select_related(
        'student_fee__student__user', 'student_fee__fee_structure'
    ).order_by('-payment_date')[:10]

    fee_structures = FeeStructure.objects.filter(school=school)
    students = StudentProfile.objects.filter(school=school).select_related('user')
    concessions = Concession.objects.filter(student__school=school)
    
    # Announcements
    announcements = Announcement.objects.filter(school=school, target_role__in=['all', 'accountant']).order_by('-created_at')[:5]

    context = {
        'total_due_amount': total_due_amount,
        'payments_today': payments_today,
        'recent_payments': recent_payments,
        'fee_structures': fee_structures,
        'students': students,
        'concessions': concessions,
        'announcements': announcements,
    }
    return render(request, 'reports/accountant_dashboard.html', context)

@login_required
@role_required(['teacher'])
def teacher_dashboard(request):
    school = request.user.school
    teacher_prof = request.user.teacher_profile

    # Timetable
    timetable = Timetable.objects.filter(teacher=teacher_prof).select_related('class_room', 'subject')

    # Classes and subjects for the entire school to allow selecting any grade
    classes = ClassRoom.objects.filter(school=school).prefetch_related('students__user').order_by('name', 'section')
    class_subjects = ClassSubject.objects.filter(class_room__school=school).select_related('class_room', 'subject').order_by('class_room__name', 'subject__name')

    # Homeworks assigned
    homeworks = Homework.objects.filter(teacher=teacher_prof).order_by('-date_assigned')[:10]

    # Leave requests of this teacher
    leaves = LeaveRequest.objects.filter(user=request.user)

    # Announcements
    announcements = Announcement.objects.filter(school=school).filter(target_role__in=['all', 'teacher']).order_by('-created_at')[:5]

    # All teachers in this school
    all_teachers = TeacherProfile.objects.filter(school=school).select_related('user')

    context = {
        'teacher': teacher_prof,
        'timetable': timetable,
        'classes': classes,
        'class_subjects': class_subjects,
        'homeworks': homeworks,
        'leaves': leaves,
        'announcements': announcements,
        'all_teachers': all_teachers,
    }
    return render(request, 'reports/teacher_dashboard.html', context)

@login_required
@role_required(['student'])
def student_dashboard(request):
    school = request.user.school
    student_prof = request.user.student_profile
    class_room = student_prof.class_room

    # Timetable
    timetable = []
    if class_room:
        timetable = Timetable.objects.filter(class_room=class_room).select_related('subject', 'teacher__user')

    # Attendance
    attendances = Attendance.objects.filter(student=student_prof)
    total_days = attendances.count()
    present_days = attendances.filter(status='present').count()
    attendance_rate = (present_days / total_days * 100) if total_days > 0 else 100.0

    # Homework assignments
    homeworks = []
    if class_room:
        homeworks = Homework.objects.filter(class_room=class_room).order_by('-due_date')[:10]

    # Student Marks
    marks = Mark.objects.filter(student=student_prof).select_related('exam_schedule__subject', 'exam_schedule__exam')

    # Fees due
    fees = StudentFee.objects.filter(student=student_prof).select_related('fee_structure')

    # Bus assignment
    bus_assignment = StudentBusAssignment.objects.filter(student=student_prof).select_related('route__bus', 'stop').first()

    # Announcements
    announcements = Announcement.objects.filter(school=school).filter(target_role__in=['all', 'student']).order_by('-created_at')[:5]

    context = {
        'student': student_prof,
        'class_room': class_room,
        'timetable': timetable,
        'attendance_rate': round(attendance_rate, 1),
        'homeworks': homeworks,
        'marks': marks,
        'fees': fees,
        'bus_assignment': bus_assignment,
        'announcements': announcements,
    }
    return render(request, 'reports/student_dashboard.html', context)

@login_required
@role_required(['parent'])
def parent_dashboard(request):
    school = request.user.school
    parent_prof = request.user.parent_profile

    # Fetch all children linked to this parent
    children = StudentProfile.objects.filter(parent=parent_prof).select_related('user', 'class_room')

    children_data = []
    for child in children:
        # Get timetable
        timetable = []
        if child.class_room:
            timetable = Timetable.objects.filter(class_room=child.class_room).select_related('subject', 'teacher__user')

        # Get attendance rate
        child_att = Attendance.objects.filter(student=child)
        tot = child_att.count()
        pres = child_att.filter(status='present').count()
        att_rate = (pres / tot * 100) if tot > 0 else 95.0

        # Get homework
        hw = []
        if child.class_room:
            hw = Homework.objects.filter(class_room=child.class_room).order_by('-due_date')[:5]

        # Get marks
        marks = Mark.objects.filter(student=child).select_related('exam_schedule__subject')

        # Get fees
        fees = StudentFee.objects.filter(student=child).select_related('fee_structure')

        # Bus assignment
        bus_assignment = StudentBusAssignment.objects.filter(student=child).select_related('route__bus', 'stop').first()

        children_data.append({
            'profile': child,
            'timetable': timetable,
            'attendance_rate': round(att_rate, 1),
            'homeworks': hw,
            'marks': marks,
            'fees': fees,
            'bus_assignment': bus_assignment
        })

    # Announcements
    announcements = Announcement.objects.filter(school=school).filter(target_role__in=['all', 'parent']).order_by('-created_at')[:5]

    context = {
        'parent': parent_prof,
        'children_data': children_data,
        'announcements': announcements,
    }
    return render(request, 'reports/parent_dashboard.html', context)

@login_required
def subscription_plans_view(request):
    school = request.user.school
    
    # Handle country switch on GET or POST
    country = request.POST.get('country') or request.GET.get('country')
    if country:
        request.session['selected_country'] = country
        return redirect('subscription_plans_view')

    if request.method == 'POST':
        # Handle plan upgrade
        plan_code = request.POST.get('plan_code')
        if plan_code:
            from schools.models import SubscriptionPlan
            new_plan = SubscriptionPlan.objects.filter(code=plan_code).first()
            if new_plan:
                school.plan = new_plan
                school.save()
                from django.contrib import messages
                messages.success(request, f"Successfully switched {school.name} to the {new_plan.name}!")
                return redirect('subscription_plans_view')

    selected_country = request.session.get('selected_country', 'IN')
    
    country_currencies = {
        'IN': {'name': 'India', 'symbol': '₹', 'silver': '50,000', 'gold': '75,000', 'platinum': '1,00,000', 'tax': 'GST'},
        'US': {'name': 'United States', 'symbol': '$', 'silver': '699', 'gold': '999', 'platinum': '1,399', 'tax': 'Sales Tax'},
        'GB': {'name': 'United Kingdom', 'symbol': '£', 'silver': '599', 'gold': '849', 'platinum': '1,199', 'tax': 'VAT'},
        'CA': {'name': 'Canada', 'symbol': 'C$', 'silver': '899', 'gold': '1,299', 'platinum': '1,799', 'tax': 'HST/GST'},
        'EU': {'name': 'Europe', 'symbol': '€', 'silver': '649', 'gold': '899', 'platinum': '1,249', 'tax': 'VAT'},
    }
    
    active_currency = country_currencies.get(selected_country, country_currencies['IN'])

    from schools.models import SubscriptionPlan
    plans = SubscriptionPlan.objects.all().order_by('monthly_price')
    return render(request, 'reports/subscription_plans.html', {
        'school': school,
        'plans': plans,
        'school_plan': school.plan.code.lower() if school.plan else 'silver',
        'selected_country': selected_country,
        'country_currencies': country_currencies,
        'active_currency': active_currency,
    })
