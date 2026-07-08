from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Import views
from accounts.views import login_view, logout_view, dashboard_redirect
from reports.views import (
    admin_dashboard, principal_dashboard, accountant_dashboard,
    teacher_dashboard, student_dashboard, parent_dashboard,
    subscription_plans_view
)
from finance.views import record_payment, assign_concession
from ocr_app.views import upload_ocr, review_ocr, approve_ocr
from transport.views import bus_tracking_map, get_bus_live_coords
from attendance_app.views import record_attendance, download_attendance_csv
from marks_app.views import record_marks
from homework_app.views import create_homework, submit_homework
from leave_app.views import request_leave, approve_leave

urlpatterns = [
    path('admin-django/', admin.site.urls),
    
    # Auth urls
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
    
    # Dashboard urls
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/principal/', principal_dashboard, name='principal_dashboard'),
    path('dashboard/accountant/', accountant_dashboard, name='accountant_dashboard'),
    path('dashboard/teacher/', teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/student/', student_dashboard, name='student_dashboard'),
    path('dashboard/parent/', parent_dashboard, name='parent_dashboard'),
    
    # Finance urls
    path('finance/payment/', record_payment, name='record_payment'),
    path('finance/concession/', assign_concession, name='assign_concession'),
    
    # OCR urls
    path('ocr/upload/', upload_ocr, name='upload_ocr'),
    path('ocr/review/<int:doc_id>/', review_ocr, name='review_ocr'),
    path('ocr/approve/<int:doc_id>/', approve_ocr, name='approve_ocr'),
    
    # Transport urls
    path('transport/map/', bus_tracking_map, name='bus_tracking_map'),
    path('transport/bus-coords/<int:bus_id>/', get_bus_live_coords, name='get_bus_live_coords'),
    
    # Core Actions urls
    path('academics/attendance/', record_attendance, name='record_attendance'),
    path('academics/attendance/download/', download_attendance_csv, name='download_attendance_csv'),
    path('academics/marks/', record_marks, name='record_marks'),
    path('academics/homework/create/', create_homework, name='create_homework'),
    path('academics/homework/submit/', submit_homework, name='submit_homework'),
    
    # Leave urls
    path('leave/request/', request_leave, name='request_leave'),
    path('leave/approve/<int:leave_id>/', approve_leave, name='approve_leave'),
    
    # Subscription & Plans
    path('subscription/plans/', subscription_plans_view, name='subscription_plans_view'),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
