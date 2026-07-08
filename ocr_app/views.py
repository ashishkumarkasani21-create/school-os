import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import OCRDocument, OCRExtractionResult
from .ocr_service import extract_document_data
from accounts.models import User, StudentProfile, ParentProfile
from finance.models import StudentFee, Payment, Receipt
from marks_app.models import Mark
from academics.models import ClassRoom, ExamSchedule, Subject

@login_required
def upload_ocr(request):
    # Admin, principal, accountant always have access
    # Teachers can access OCR only on Gold/Platinum plan schools
    user = request.user
    school_plan = user.school.plan.code.lower() if (user.school and user.school.plan) else 'silver'
    teacher_has_ocr = user.role == 'teacher' and school_plan in ['gold', 'platinum']
    if user.role not in ['admin', 'principal', 'accountant'] and not teacher_has_ocr:
        messages.error(request, "Unauthorized to access OCR features.")
        return redirect('dashboard_redirect')


    if request.method == 'POST' and request.FILES.get('document_file'):
        doc_type = request.POST.get('document_type')
        uploaded_file = request.FILES.get('document_file')

        # Create OCRDocument
        ocr_doc = OCRDocument.objects.create(
            school=request.user.school,
            uploaded_by=request.user,
            document_type=doc_type,
            file=uploaded_file,
            status='pending'
        )

        # Trigger OCR Processing Service
        file_path = ocr_doc.file.path
        extracted_text, raw_json_data = extract_document_data(file_path, doc_type)

        # Save Extraction Results
        OCRExtractionResult.objects.create(
            ocr_document=ocr_doc,
            extracted_text=extracted_text,
            raw_json_data=raw_json_data
        )

        messages.success(request, f"OCR Document uploaded and processed. Data ready for review.")
        return redirect('review_ocr', doc_id=ocr_doc.id)
        
    return redirect('dashboard_redirect')

@login_required
def review_ocr(request, doc_id):
    ocr_doc = get_object_or_404(OCRDocument, id=doc_id, school=request.user.school)
    extraction = get_object_or_404(OCRExtractionResult, ocr_document=ocr_doc)

    if request.method == 'POST':
        # Admin or Accountant changes the fields in the UI
        # and we update the JSON
        updated_json = {}
        for key, value in request.POST.items():
            if key not in ['csrfmiddlewaretoken']:
                # Handle nested structure for marksheets if needed
                if key.startswith('subject_name_'):
                    idx = key.split('_')[-1]
                    subj_marks = request.POST.get(f'subject_marks_{idx}')
                    if 'subjects' not in updated_json:
                        updated_json['subjects'] = []
                    updated_json['subjects'].append({
                        'name': value,
                        'marks': int(subj_marks or 0)
                    })
                elif key.startswith('subject_marks_'):
                    pass
                else:
                    updated_json[key] = value

        extraction.raw_json_data = updated_json
        extraction.save()
        messages.success(request, "Extracted data modifications saved.")
        
        # If the user clicked "Approve and Integrate"
        if 'approve_integrate' in request.POST:
            return approve_ocr(request, ocr_doc.id)

    # Render review page
    return render(request, 'ocr_app/review.html', {
        'doc': ocr_doc,
        'extraction': extraction,
        'json_data': extraction.raw_json_data
    })

@login_required
def approve_ocr(request, doc_id):
    ocr_doc = get_object_or_404(OCRDocument, id=doc_id, school=request.user.school)
    extraction = ocr_doc.extraction_result
    data = extraction.raw_json_data

    try:
        if ocr_doc.document_type == 'admission':
            # Create a user + student profile from admission form data
            username = data.get('username') or data.get('student_name', 'student_user').lower().replace(' ', '')
            email = f"{username}@school.edu"
            
            # Create user account
            student_user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'role': 'student',
                    'school': ocr_doc.school
                }
            )
            if created:
                student_user.set_password('school123')
                student_user.save()

            # Assign class
            class_applied = data.get('class_applied', 'Grade 5')
            classroom = ClassRoom.objects.filter(school=ocr_doc.school, name__icontains=class_applied).first()
            if not classroom:
                classroom = ClassRoom.objects.filter(school=ocr_doc.school).first()

            # Create/update profile
            dob = timezone.now().date()
            dob_str = data.get('date_of_birth')
            if dob_str:
                try:
                    dob = timezone.datetime.strptime(dob_str, '%Y-%m-%d').date()
                except ValueError:
                    pass

            student_id = data.get('student_id') or f"STU-{student_user.id:04d}"
            StudentProfile.objects.update_or_create(
                user=student_user,
                defaults={
                    'school': ocr_doc.school,
                    'student_id': student_id,
                    'class_room': classroom,
                    'date_of_birth': dob,
                    'roll_number': str(100 + student_user.id)
                }
            )
            messages.success(request, f"Successfully created Student Profile for {data.get('student_name')}.")

        elif ocr_doc.document_type == 'marksheet':
            # Record marks
            student_name = data.get('student_name', '')
            student = StudentProfile.objects.filter(school=ocr_doc.school, user__username__icontains=student_name.replace(' ', '')).first()
            if not student:
                student = StudentProfile.objects.filter(school=ocr_doc.school).first()

            if student:
                subjects_data = data.get('subjects', [])
                for subj in subjects_data:
                    subj_obj = Subject.objects.filter(school=ocr_doc.school, name__icontains=subj['name']).first()
                    if subj_obj:
                        exam_sched = ExamSchedule.objects.filter(class_room=student.class_room, subject=subj_obj).first()
                        if exam_sched:
                            Mark.objects.update_or_create(
                                student=student,
                                exam_schedule=exam_sched,
                                defaults={'marks_obtained': subj['marks']}
                            )
                messages.success(request, f"Grades from Marksheet successfully injected into marks registry for {student.user.username}.")
            else:
                messages.error(request, "Student matching the marksheet name was not found.")

        elif ocr_doc.document_type == 'receipt':
            # Record a fee payment
            student_name = data.get('student_name', '')
            student = StudentProfile.objects.filter(school=ocr_doc.school, user__username__icontains=student_name.replace(' ', '')).first()
            if not student:
                student = StudentProfile.objects.filter(school=ocr_doc.school).first()

            if student:
                fee_invoice = StudentFee.objects.filter(student=student, status='unpaid').first()
                if fee_invoice:
                    amt = float(data.get('amount', 0.00))
                    payment = Payment.objects.create(
                        student_fee=fee_invoice,
                        amount_paid=amt,
                        payment_method=data.get('payment_method', 'card'),
                        transaction_id=data.get('receipt_number', '')
                    )
                    Receipt.objects.create(
                        payment=payment,
                        receipt_number=data.get('receipt_number', f"REC-{payment.id:04d}")
                    )
                    fee_invoice.paid_amount = float(fee_invoice.paid_amount) + amt
                    fee_invoice.update_status()
                    messages.success(request, f"Fee payment of ${amt:.2f} successfully recorded from receipt OCR.")
                else:
                    messages.warning(request, "No unpaid fee invoice found for this student.")
            else:
                messages.error(request, "Student matching the receipt name was not found.")

        ocr_doc.status = 'approved'
        ocr_doc.save()

    except Exception as e:
        messages.error(request, f"Error integrating document data: {e}")
        return redirect('review_ocr', doc_id=ocr_doc.id)

    return redirect('dashboard_redirect')
