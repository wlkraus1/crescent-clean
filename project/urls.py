from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth import get_user_model

def home(_):
    return HttpResponse("Crescent is live. Visit /bootstrap once, then /admin to log in.")

def bootstrap(request):
    import os
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # Fallbacks so you can get in even if Render env vars aren’t set
    email = os.environ.get("OWNER_EMAIL", "Tyler.Krause@icloud.com")
    pwd = os.environ.get("OWNER_PASSWORD", "admin")

    if not User.objects.filter(username=email).exists():
        User.objects.create_superuser(username=email, email=email, password=pwd)
        return HttpResponse(f"Owner created for {email}. Now go to /admin")
    return HttpResponse("Owner already exists. Go to /admin")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("bootstrap", bootstrap),
    path("", home),
]
