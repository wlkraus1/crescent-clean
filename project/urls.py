from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth import get_user_model

def home(_):
    return HttpResponse("Crescent is live. Visit /bootstrap once, then /admin to log in.")

def bootstrap(request):
    import os
    User = get_user_model()
    email = os.environ.get("OWNER_EMAIL")
    pwd = os.environ.get("OWNER_PASSWORD")
    if not email or not pwd:
        return HttpResponse("Set OWNER_EMAIL and OWNER_PASSWORD env vars, then reload.", status=500)
    if not User.objects.filter(username=email).exists():
        User.objects.create_superuser(username=email, email=email, password=pwd)
        return HttpResponse(f"Owner created for {email}. Now go to /admin")
    return HttpResponse("Owner already exists. Go to /admin")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bootstrap", bootstrap),
    path("", home),
]
