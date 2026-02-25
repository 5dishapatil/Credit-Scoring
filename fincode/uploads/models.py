from django.db import models

class FinancialUpload(models.Model):
    business_name = models.CharField(max_length=255)
    gstin = models.CharField(max_length=15)
    pan = models.CharField(max_length=10)

    file = models.FileField(upload_to='financial_records/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
