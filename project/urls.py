from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth import get_user_model
import os

def home(_):
    return HttpResponse("Crescent CRM is live. Visit /crm or /portal.")

def bootstrap(request):
    User = get_user_model()
    email = os.environ.get("OWNER_EMAIL", "Tyler.Krause@icloud.com")
    pwd = os.environ.get("OWNER_PASSWORD", "Temp!2345")
    if not User.objects.filter(username=email).exists():
        User.objects.create_superuser(username=email, email=email, password=pwd)
        return HttpResponse(f"Owner created for {email}. Now go to /admin")
    return HttpResponse("Owner already exists. Go to /admin")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bootstrap", bootstrap),
    path("crm/", include("crm.urls")),      # CRM section
    path("portal/", include("portal.urls")),  # Client Portal section
    path("", home),
]
