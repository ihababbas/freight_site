from django.db import models

class Submission(models.Model):
    SERVICE_CHOICES = [
        ("sea", "Sea Freight"),
        ("air", "Air Freight"),
        ("land", "Land Freight"),
        ("other", "Others"),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    company = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=10, choices=SERVICE_CHOICES)
    details = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.get_service_display()}"

    class Meta:
        ordering = ("-created_at",)
