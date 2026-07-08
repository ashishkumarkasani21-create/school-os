from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import LeaveRequest
import datetime

@login_required
def request_leave(request):
    if request.method == 'POST':
        start_str = request.POST.get('start_date')
        end_str = request.POST.get('end_date')
        reason = request.POST.get('reason')

        try:
            start_date = datetime.datetime.strptime(start_str, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            return redirect('dashboard_redirect')

        LeaveRequest.objects.create(
            user=request.user,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status='pending'
        )
        messages.success(request, "Leave request submitted successfully. Awaiting approval.")
        
    return redirect('dashboard_redirect')

@login_required
def approve_leave(request, leave_id):
    if request.user.role not in ['principal', 'admin']:
        messages.error(request, "Only the principal or admins can approve leave requests.")
        return redirect('dashboard_redirect')

    leave = get_object_or_404(LeaveRequest, id=leave_id, user__school=request.user.school)
    
    if request.method == 'POST':
        action = request.POST.get('action')  # approve / reject
        remarks = request.POST.get('remarks', '')

        if action == 'approve':
            leave.status = 'approved'
            msg = "Leave request approved."
        else:
            leave.status = 'rejected'
            msg = "Leave request rejected."

        leave.approved_by = request.user
        leave.remarks = remarks
        leave.save()
        messages.success(request, msg)

    return redirect('dashboard_redirect')
