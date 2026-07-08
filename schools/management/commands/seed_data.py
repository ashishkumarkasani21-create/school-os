import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from schools.models import SubscriptionPlan, School, SchoolSubscription
from accounts.models import (
    User, PrincipalProfile, TeacherProfile, StudentProfile, ParentProfile, AccountantProfile
)
from academics.models import ClassRoom, Subject, ClassSubject, Timetable, Exam, ExamSchedule
from attendance_app.models import Attendance
from homework_app.models import Homework
from marks_app.models import Mark
from finance.models import FeeStructure, StudentFee, Payment, Receipt
from transport.models import Bus, Driver, Route, Stop, StudentBusAssignment
from communication.models import Announcement, Complaint
from leave_app.models import LeaveRequest

class Command(BaseCommand):
    help = 'Seeds database with default subscription plans, starter/growth/premium schools, and full role profiles.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding Subscription Plans...")
        
        # 1. Create Subscription Plans
        silver_plan, _ = SubscriptionPlan.objects.get_or_create(
            code='silver',
            defaults={
                'name': 'Silver Plan',
                'monthly_price': 49.00,
                'yearly_price': 490.00,
                'features_json': '["academics_basic", "attendance", "homework", "announcements", "fee_view"]'
            }
        )
        gold_plan, _ = SubscriptionPlan.objects.get_or_create(
            code='gold',
            defaults={
                'name': 'Gold Plan',
                'monthly_price': 149.00,
                'yearly_price': 1490.00,
                'features_json': '["academics_basic", "attendance", "homework", "announcements", "fee_view", "accounting_reports", "timetable", "exams", "leave_requests", "ocr_basic", "bus_static"]'
            }
        )
        platinum_plan, _ = SubscriptionPlan.objects.get_or_create(
            code='platinum',
            defaults={
                'name': 'Platinum Plan',
                'monthly_price': 299.00,
                'yearly_price': 2990.00,
                'features_json': '["academics_basic", "attendance", "homework", "announcements", "fee_view", "accounting_reports", "timetable", "exams", "leave_requests", "ocr_basic", "bus_static", "ocr_advanced", "live_bus_tracking", "advanced_analytics", "audit_logs"]'
            }
        )

        # 2. Setup Three Schools
        self.stdout.write("Creating Schools...")
        schools_data = [
            ('Silver', 'silver', silver_plan),
            ('Gold', 'gold', gold_plan),
            ('Platinum', 'platinum', platinum_plan),
        ]
        
        schools = {}
        for name, code, plan in schools_data:
            sch, created = School.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'plan': plan,
                    'is_active': True,
                    'address': f"100 Education Way, {name} Campus",
                    'phone': '1-800-555-0100',
                    'email': f"info@{code}.edu"
                }
            )
            schools[code] = sch
            
            # Create subscription
            SchoolSubscription.objects.get_or_create(
                school=sch,
                plan=plan,
                defaults={
                    'start_date': timezone.now().date(),
                    'end_date': timezone.now().date() + datetime.timedelta(days=365),
                    'status': 'active'
                }
            )

        # 3. Create Users and Profiles for each School
        self.stdout.write("Creating Users & Profiles...")
        roles = ['admin', 'principal', 'accountant', 'teacher', 'student', 'parent']
        
        for code, school in schools.items():
            users = {}
            for role in roles:
                uname = f"{role}_{code.replace('-', '_')}"
                user, created = User.objects.get_or_create(
                    username=uname,
                    defaults={
                        'first_name': role.capitalize(),
                        'last_name': school.name.split()[0],
                        'email': f"{uname}@school.edu",
                        'role': role,
                        'school': school,
                        'is_staff': True if role == 'admin' else False
                    }
                )
                if created or not user.has_usable_password():
                    user.set_password('school123')
                    user.save()
                users[role] = user

            # Principal Profile
            PrincipalProfile.objects.get_or_create(
                user=users['principal'],
                defaults={'school': school, 'qualification': 'Ph.D. in Education Administration', 'bio': f"Principal of {school.name}."}
            )
            # Accountant Profile
            AccountantProfile.objects.get_or_create(
                user=users['accountant'],
                defaults={'school': school, 'employee_id': f"ACC-{school.id:02d}"}
            )
            # Teacher Profile
            teacher_prof, _ = TeacherProfile.objects.get_or_create(
                user=users['teacher'],
                defaults={'school': school, 'employee_id': f"TCH-{school.id:02d}", 'designation': 'Senior Faculty', 'qualification': 'Master of Arts in Education'}
            )
            # Parent Profile
            parent_prof, _ = ParentProfile.objects.get_or_create(
                user=users['parent'],
                defaults={'school': school, 'occupation': 'Software Engineer', 'address': '456 Residential Avenue'}
            )
            
            # Academics Setup: ClassRoom & Subject
            classroom, _ = ClassRoom.objects.get_or_create(
                school=school,
                name='Grade 10',
                section='A',
                defaults={'class_teacher': teacher_prof}
            )
            
            math_sub, _ = Subject.objects.get_or_create(
                school=school,
                name='Mathematics',
                code='MATH10'
            )
            english_sub, _ = Subject.objects.get_or_create(
                school=school,
                name='English Literature',
                code='ENG10'
            )
            science_sub, _ = Subject.objects.get_or_create(
                school=school,
                name='Science',
                code='SCI10'
            )
            social_sub, _ = Subject.objects.get_or_create(
                school=school,
                name='Social Studies',
                code='SOC10'
            )
            cs_sub, _ = Subject.objects.get_or_create(
                school=school,
                name='Computer Science',
                code='COMP10'
            )

            ClassSubject.objects.get_or_create(
                class_room=classroom,
                subject=math_sub,
                defaults={'teacher': teacher_prof}
            )
            ClassSubject.objects.get_or_create(
                class_room=classroom,
                subject=english_sub,
                defaults={'teacher': teacher_prof}
            )
            ClassSubject.objects.get_or_create(
                class_room=classroom,
                subject=science_sub,
                defaults={'teacher': teacher_prof}
            )
            ClassSubject.objects.get_or_create(
                class_room=classroom,
                subject=social_sub,
                defaults={'teacher': teacher_prof}
            )
            ClassSubject.objects.get_or_create(
                class_room=classroom,
                subject=cs_sub,
                defaults={'teacher': teacher_prof}
            )

            # Timetable Setup
            Timetable.objects.get_or_create(
                class_room=classroom,
                subject=math_sub,
                teacher=teacher_prof,
                day_of_week='monday',
                defaults={'start_time': datetime.time(9, 0), 'end_time': datetime.time(10, 0)}
            )
            Timetable.objects.get_or_create(
                class_room=classroom,
                subject=english_sub,
                teacher=teacher_prof,
                day_of_week='monday',
                defaults={'start_time': datetime.time(10, 15), 'end_time': datetime.time(11, 15)}
            )

            # Student Profile
            student_prof, _ = StudentProfile.objects.get_or_create(
                user=users['student'],
                defaults={
                    'school': school,
                    'student_id': f"STU-{school.id:02d}",
                    'class_room': classroom,
                    'roll_number': '12',
                    'date_of_birth': datetime.date(2010, 6, 15),
                    'parent': parent_prof
                }
            )

            # Attendance Log
            Attendance.objects.get_or_create(
                student=student_prof,
                date=timezone.localdate(),
                defaults={'status': 'present', 'remarks': 'On time'}
            )
            Attendance.objects.get_or_create(
                student=student_prof,
                date=timezone.localdate() - datetime.timedelta(days=1),
                defaults={'status': 'present'}
            )

            # Homework Setup
            Homework.objects.get_or_create(
                class_room=classroom,
                subject=math_sub,
                teacher=teacher_prof,
                title='Quadratic Equations Practice',
                defaults={
                    'description': 'Solve questions 1 to 10 from Chapter 4 of the algebra textbook.',
                    'due_date': timezone.localdate() + datetime.timedelta(days=2)
                }
            )

            # Exam & Exam Schedule
            exam, _ = Exam.objects.get_or_create(
                school=school,
                name='Midterm Assessment',
                defaults={
                    'start_date': timezone.localdate() + datetime.timedelta(days=10),
                    'end_date': timezone.localdate() + datetime.timedelta(days=15)
                }
            )
            exam_sched, _ = ExamSchedule.objects.get_or_create(
                exam=exam,
                class_room=classroom,
                subject=math_sub,
                date=timezone.localdate() + datetime.timedelta(days=10),
                defaults={
                    'start_time': datetime.time(9, 0),
                    'end_time': datetime.time(11, 0),
                    'max_marks': 100
                }
            )

            # Record a Grade
            Mark.objects.get_or_create(
                student=student_prof,
                exam_schedule=exam_sched,
                defaults={'marks_obtained': 88.5, 'remarks': 'Great effort!'}
            )

            # Finance: Fee Structures & Student Fees
            fee_struct, _ = FeeStructure.objects.get_or_create(
                school=school,
                fee_type='Tuition Fee',
                defaults={'amount': 1500.00, 'class_room': classroom}
            )
            
            student_fee, _ = StudentFee.objects.get_or_create(
                student=student_prof,
                fee_structure=fee_struct,
                defaults={
                    'due_date': timezone.localdate() + datetime.timedelta(days=30),
                    'amount': 1500.00,
                    'paid_amount': 0.00,
                    'status': 'unpaid'
                }
            )

            # Record a Payment
            if school.plan.code in ['growth', 'premium']:
                payment = Payment.objects.create(
                    student_fee=student_fee,
                    amount_paid=500.00,
                    payment_method='online',
                    transaction_id=f'TXN-{school.id}-904123'
                )
                Receipt.objects.create(
                    payment=payment,
                    receipt_number=f'REC-{school.id}-0001'
                )
                student_fee.paid_amount = 500.00
                student_fee.update_status()

            # Transport Setup (Buses, Driver, Routes, Stops)
            bus, _ = Bus.objects.get_or_create(
                school=school,
                bus_number=f'BUS-{school.id:02d}X',
                defaults={'capacity': 40, 'status': 'active'}
            )
            driver, _ = Driver.objects.get_or_create(
                school=school,
                name='Michael Driver',
                defaults={'phone': '+1 555-0155', 'license_number': f'LIC-{school.id}-992'}
            )
            route, _ = Route.objects.get_or_create(
                school=school,
                name='Downtown East Route',
                defaults={'bus': bus, 'driver': driver}
            )

            # Stop Coordinates near Los Angeles downtown
            stops_data = [
                ('East Terminal Start', 34.0522, -118.2437, datetime.time(7, 30), 1),
                ('Main Street Stop', 34.0582, -118.2520, datetime.time(7, 45), 2),
                ('Grand Avenue Stop', 34.0620, -118.2610, datetime.time(8, 00), 3),
                ('Elite School Campus Entrance', 34.0700, -118.2700, datetime.time(8, 20), 4),
            ]
            for name, lat, lng, arr_time, seq in stops_data:
                Stop.objects.get_or_create(
                    route=route,
                    name=name,
                    defaults={'latitude': lat, 'longitude': lng, 'arrival_time': arr_time, 'sequence_order': seq}
                )

            # Assign Student to Route & Stop
            Stop_obj = Stop.objects.filter(route=route, sequence_order=2).first()
            if Stop_obj:
                StudentBusAssignment.objects.get_or_create(
                    student=student_prof,
                    defaults={'route': route, 'stop': Stop_obj}
                )

            # Leave Requests
            LeaveRequest.objects.get_or_create(
                user=users['student'],
                start_date=timezone.localdate() + datetime.timedelta(days=5),
                end_date=timezone.localdate() + datetime.timedelta(days=6),
                defaults={'reason': 'Family wedding ceremony', 'status': 'pending'}
            )

            # Complaints / Communication
            Complaint.objects.get_or_create(
                school=school,
                created_by=users['parent'],
                title='Late school bus notification delay',
                defaults={'description': 'The bus was 20 minutes late on Monday and no SMS warning was sent out to parents.', 'status': 'pending'}
            )

            # Announcements
            Announcement.objects.get_or_create(
                school=school,
                title='Annual Sports Meet 2026 Rescheduled',
                created_by=users['admin'],
                defaults={
                    'content': 'Please note that due to weather forecasts, the annual sports tournament scheduled for next week is shifted to August 20th. Active lists remain unchanged.',
                    'target_role': 'all'
                }
            )

        # 4. Seed custom teachers requested by user: Olivia, Mokshith, Ashish, Swapna, John
        self.stdout.write("Seeding custom teachers (Olivia, Mokshith, Ashish, Swapna, John)...")
        silver_school = schools.get('silver')
        gold_school = schools.get('gold')
        plat_school = schools.get('platinum')

        custom_teachers = [
            # Platinum school
            ('Olivia',   'Smith',   'teacher_olivia',   plat_school,   'Grade 9',  'A', 'SCI10'),
            ('Mokshith', 'Kumar',   'teacher_mokshith', plat_school,   'Grade 10', 'B', 'MATH10'),
            ('Sophia',   'Davis',   'teacher_sophia',   plat_school,   'Grade 11', 'A', 'ENG10'),
            ('Liam',     'Wilson',  'teacher_liam',     plat_school,   'Grade 12', 'A', 'COMP10'),
            # Gold school
            ('Ashish',   'Kasani',  'teacher_ashish',   gold_school,   'Grade 8',  'A', 'MATH10'),
            ('Swapna',   'Reddy',   'teacher_swapna',   gold_school,   'Grade 7',  'B', 'SOC10'),
            ('Noah',     'Taylor',  'teacher_noah',     gold_school,   'Grade 9',  'B', 'SCI10'),
            ('Emma',     'Thomas',  'teacher_emma',     gold_school,   'Grade 10', 'A', 'ENG10'),
            # Silver school
            ('John',     'Martin',  'teacher_john',     silver_school, 'Grade 6',  'A', 'ENG10'),
            ('Lucas',    'Moore',   'teacher_lucas',    silver_school, 'Grade 8',  'B', 'MATH10'),
            ('Isabella', 'Anderson','teacher_isabella', silver_school, 'Grade 7',  'A', 'SCI10'),
        ]

        for first, last, username, school, class_name, section, sub_code in custom_teachers:
            if not school:
                continue
            # Create user
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': f'{username}@schoolos.edu',
                    'role': 'teacher',
                    'school': school,
                }
            )
            if created or not user.has_usable_password():
                user.set_password('school123')
                user.save()

            # Create classroom if not exist
            classroom, _ = ClassRoom.objects.get_or_create(
                school=school,
                name=class_name,
                section=section,
            )

            # Create teacher profile
            profile, _ = TeacherProfile.objects.get_or_create(
                user=user,
                defaults={'school': school}
            )

            # Assign teacher to classroom
            classroom.class_teacher = profile
            classroom.save()

            # Fetch subject and assign to teacher in this classroom
            subject = Subject.objects.filter(school=school, code=sub_code).first()
            if subject:
                ClassSubject.objects.get_or_create(
                    class_room=classroom,
                    subject=subject,
                    defaults={'teacher': profile}
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with all roles, classes, fee tables, bus routes, and custom teachers!'))

