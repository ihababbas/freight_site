from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from .models import Submission
from .serializers import SubmissionSerializer

@api_view(["POST"])
def submit_quote(request):
    serializer = SubmissionSerializer(data=request.data)
    if serializer.is_valid():
        submission = serializer.save()

        # تجهيز الإيميل
        service_label = submission.get_service_display()
        subject = f"New Freight Inquiry - {service_label}"
        body = (
            f"Full Name: {submission.full_name}\n"
            f"Email: {submission.email}\n"
            f"Company: {submission.company}\n"
            f"Phone: {submission.phone}\n"
            f"Service Required: {service_label}\n\n"
            f"Project Details:\n{submission.details}\n"
            f"\n---\n"
            f"Submission ID: {submission.id}\n"
        )

        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.QUOTES_RECEIVER_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                {"error": f"Submission saved but email failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
