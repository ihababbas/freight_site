from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .forms import QuoteForm, SERVICE_CHOICES
from .models import Submission   # إذا بدك تخزن الطلبات

def contact_view(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # --- 1) تخزين الطلب في قاعدة البيانات ---
            submission = Submission.objects.create(
                full_name=data["full_name"],
                email=data["email"],
                company=data.get("company", ""),
                phone=data["phone"],
                service=data["service"],
                details=data["details"],
            )

            # --- 2) تجهيز الإيميل ---
            service_map = dict(SERVICE_CHOICES)
            service_label = service_map.get(data["service"], data["service"])

            subject = f"New Freight Inquiry - {service_label}"
            body = (
                f"Full Name: {data['full_name']}\n"
                f"Email: {data['email']}\n"
                f"Company: {data.get('company','')}\n"
                f"Phone: {data['phone']}\n"
                f"Service Required: {service_label}\n\n"
                f"Project Details:\n{data['details']}\n"
                f"\n---\n"
                f"Submission ID: {submission.id}\n"
            )

            to_emails = [getattr(settings, "QUOTES_RECEIVER_EMAIL", settings.DEFAULT_FROM_EMAIL)]

            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    to_emails,
                    fail_silently=False,
                )
                messages.success(request, "✅ تم إرسال الطلب بنجاح — سنتواصل معك قريبًا.")
            except Exception as e:
                messages.error(request, f"⚠️ حدث خطأ أثناء إرسال البريد: {e}")

            return redirect("contact:contact")
        else:
            messages.error(request, "الرجاء التحقق من الحقول بالأسفل.")
    else:
        form = QuoteForm()

    return render(request, "contact/form.html", {"form": form})
