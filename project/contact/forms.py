from django import forms
import re

SERVICE_CHOICES = [
    ("", "Select a service"),
    ("sea", "Sea Freight"),
    ("air", "Air Freight"),
    ("land", "Land Freight"),
    ("other", "Others"),
]

class QuoteForm(forms.Form):
    full_name = forms.CharField(label="Full Name", max_length=100)
    email = forms.EmailField(label="Email Address")
    company = forms.CharField(label="Company Name", max_length=120, required=False)
    phone = forms.CharField(label="Phone Number", max_length=20)
    service = forms.ChoiceField(label="Service Required", choices=SERVICE_CHOICES)
    details = forms.CharField(label="Project Details", widget=forms.Textarea, max_length=3000)

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        # مثال بسيط: دعم الأردن (+9627…) أو أرقام دولية تبدأ بـ +
        if not re.match(r"^(\+9627\d{7,8}|\+\d{7,15}|0\d{7,15})$", phone):
            raise forms.ValidationError("رقم الهاتف غير صحيح.")
        return phone

    def clean_service(self):
        s = self.cleaned_data["service"]
        if not s:
            raise forms.ValidationError("الرجاء اختيار الخدمة.")
        return s
