from django.urls import path
from .api_views import submit_quote
from .views import contact_view

app_name = "contact"

urlpatterns = [
    path("", contact_view, name="contact"),        # الفورم العادي
    path("api/quote/", submit_quote, name="api_quote"),  # الـ endpoint
]
