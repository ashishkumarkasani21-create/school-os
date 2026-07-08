from django.db import models
from schools.models import School
from accounts.models import StudentProfile
from academics.models import ClassRoom

class FeeStructure(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True, help_text="Null means global fee structure for all classes")
    fee_type = models.CharField(max_length=100)  # e.g., "Tuition Fee", "Registration Fee", "Transport Fee"
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        class_str = self.class_room.name if self.class_room else "All Classes"
        return f"{self.fee_type} - {class_str}: ${self.amount}"

class StudentFee(models.Model):
    STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
    )
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='fees')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    concession_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid')

    def __str__(self):
        return f"{self.student.user.username} - {self.fee_structure.fee_type} (${self.amount})"

    @property
    def net_amount(self):
        return max(self.amount - self.concession_amount, 0)

    @property
    def balance(self):
        return max(self.net_amount - self.paid_amount, 0)

    def update_status(self):
        net = self.net_amount
        if self.paid_amount >= net:
            self.status = 'paid'
        elif self.paid_amount > 0:
            self.status = 'partially_paid'
        else:
            self.status = 'unpaid'
        self.save()

class Payment(models.Model):
    METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online Payment'),
    )
    student_fee = models.ForeignKey(StudentFee, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='cash')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Payment #{self.id} for {self.student_fee.student.user.username} (${self.amount_paid})"

class Receipt(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='receipt')
    receipt_number = models.CharField(max_length=50, unique=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt {self.receipt_number}"

class Concession(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='concessions')
    fee_type = models.CharField(max_length=100, help_text="Fee type this concession applies to (e.g. Tuition Fee)")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="e.g. 10.00 for 10% discount")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Flat discount amount")
    reason = models.TextField()

    def __str__(self):
        return f"{self.student.user.username} - Concession for {self.fee_type}"
