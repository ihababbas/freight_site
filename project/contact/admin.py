from django.contrib import admin
from .models import Submission

# تخصيص عناوين لوحة التحكم
admin.site.site_header = "Freight Admin"
admin.site.site_title = "Freight Admin"
admin.site.index_title = "Dashboard"

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "service", "created_at")
    list_filter = ("service", "created_at")
    search_fields = ("full_name", "email", "phone", "company", "details")
    readonly_fields = (
        "full_name", "email", "company", "phone", "service", "details", "created_at"
    )
    date_hierarchy = "created_at"
    ordering = ("-created_at",)