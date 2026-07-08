from django.db import models
from django.conf import settings
from schools.models import School

class OCRDocument(models.Model):
    DOC_TYPES = (
        ('admission', 'Student Admission Form'),
        ('marksheet', 'Marksheet / Grade Sheet'),
        ('receipt', 'Fee Receipt'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved & Processed'),
        ('rejected', 'Rejected'),
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices=DOC_TYPES)
    file = models.FileField(upload_to='ocr_documents/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class OCRExtractionResult(models.Model):
    ocr_document = models.OneToOneField(OCRDocument, on_delete=models.CASCADE, related_name='extraction_result')
    extracted_text = models.TextField(blank=True)
    raw_json_data = models.JSONField(default=dict, blank=True, help_text="Parsed fields (e.g. name, marks, total)")

    def __str__(self):
        return f"Extraction Result for Doc ID: {self.ocr_document.id}"
