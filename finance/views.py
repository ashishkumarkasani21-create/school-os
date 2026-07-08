from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import StudentFee, Payment, Receipt, Concession, FeeStructure
from accounts.models import StudentProfile

@login_required
def record_payment(request):
    if request.user.role not in ['accountant', 'admin']:
        messages.error(request, "Only accountants or admins can record payments.")
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        fee_id = request.POST.get('student_fee_id')
        amount_paid = float(request.POST.get('amount_paid', 0.00))
        method = request.POST.get('payment_method', 'cash')
        tx_id = request.POST.get('transaction_id', '')

        student_fee = get_object_or_404(StudentFee, id=fee_id, student__school=request.user.school)

        if amount_paid <= 0:
            messages.error(request, "Amount paid must be greater than zero.")
            return redirect('dashboard_redirect')

        # Limit to remaining balance
        bal = float(student_fee.balance)
        if amount_paid > bal:
            amount_paid = bal

        # Record payment
        payment = Payment.objects.create(
            student_fee=student_fee,
            amount_paid=amount_paid,
            payment_method=method,
            transaction_id=tx_id
        )

        # Generate Receipt
        receipt_no = f"REC-{timezone.now().strftime('%Y%m%d')}-{payment.id:04d}"
        Receipt.objects.create(
            payment=payment,
            receipt_number=receipt_no
        )

        # Update fee status
        student_fee.paid_amount = float(student_fee.paid_amount) + amount_paid
        student_fee.update_status()

        messages.success(request, f"Payment of ${amount_paid:.2f} logged successfully. Receipt {receipt_no} generated.")
    
    return redirect('dashboard_redirect')

@login_required
def assign_concession(request):
    if request.user.role not in ['accountant', 'admin']:
        messages.error(request, "Only accountants or admins can assign concessions.")
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        fee_type = request.POST.get('fee_type')
        discount_amount = float(request.POST.get('discount_amount', 0.00))
        reason = request.POST.get('reason', '')

        student = get_object_or_404(StudentProfile, id=student_id, school=request.user.school)

        # Create concession
        Concession.objects.create(
            student=student,
            fee_type=fee_type,
            discount_amount=discount_amount,
            reason=reason
        )

        # Apply to matching unpaid fee invoices
        matching_fees = StudentFee.objects.filter(student=student, fee_structure__fee_type=fee_type, status='unpaid')
        for fee in matching_fees:
            fee.concession_amount = float(fee.concession_amount) + discount_amount
            fee.update_status()

        messages.success(request, f"Concession of ${discount_amount:.2f} assigned to {student.user.get_full_name() or student.user.username}.")
        
    return redirect('dashboard_redirect')
