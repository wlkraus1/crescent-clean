from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.management import call_command
from io import StringIO
import os

def home(_):
    return HttpResponse("Crescent CRM is live. Use /migrate once, then /seed. Try /portal/household/1/ and /admin.")

def bootstrap(request):
    User = get_user_model()
    email = os.environ.get("OWNER_EMAIL", "Tyler.Krause@icloud.com")
    pwd = os.environ.get("OWNER_PASSWORD", "Temp!2345")
    if not User.objects.filter(username=email).exists():
        User.objects.create_superuser(username=email, email=email, password=pwd)
        return HttpResponse(f"Owner created for {email}. Now go to /admin")
    return HttpResponse("Owner already exists. Go to /admin")

def migrate_now(request):
    from io import StringIO
    from django.conf import settings
    from django.apps import apps

    out = StringIO()
    try:
        out.write("INSTALLED_APPS:\n" + "\n".join(settings.INSTALLED_APPS) + "\n\n")
        out.write("Loaded app configs:\n" + "\n".join(a.name for a in apps.get_app_configs()) + "\n\n")

        # Ensure crm has migrations, then apply crm explicitly, then everything
        call_command("makemigrations", "crm", interactive=False, stdout=out, stderr=out, verbosity=1)
        call_command("migrate", "crm", interactive=False, stdout=out, stderr=out, verbosity=1)
        call_command("migrate", interactive=False, stdout=out, stderr=out, verbosity=1)

        out_after = StringIO()
        call_command("showmigrations", "crm", stdout=out_after, verbosity=1)
        return HttpResponse("MIGRATE OK<br><pre>" + out.getvalue() + "\nCRM migrations:\n" + out_after.getvalue() + "</pre>")
    except Exception:
        return HttpResponse("MIGRATE ERROR<br><pre>" + out.getvalue() + "</pre>", status=500)


def seed(request):
    try:
        from datetime import date, timedelta
        from crm.models import Household, Client, Account, Holding, Task, Document

        if Household.objects.exists():
            return HttpResponse("Demo already seeded.")

        today = date.today()
        nextwk = today + timedelta(days=7)

        h = Household.objects.create(
            name='[DEMO] Gump Family',
            aum_estimate=250000,
            notes='Annual review next month.'
        )
        c1 = Client.objects.create(
            household=h, first_name='Forrest', last_name='Gump',
            email='forrest@example.com', ssn_last4='1234',
            risk_score=45, kyc_status='Complete'
        )
        a1 = Account.objects.create(
            household=h, client=c1, custodian='Schwab',
            account_number_last4='6421', account_type='Brokerage',
            tax_status='Taxable', model='Core Growth', status='Active'
        )
        Holding.objects.create(
            account=a1, symbol='VOO', quantity=120, cost_basis=380.00,
            price_as_of=525.00, as_of_date=today
        )
        Task.objects.create(
            household=h, client=c1, title='Send IPS for e-sign',
            due_on=nextwk, assigned_to='Tyler Krause',
            status='Open', priority='High'
        )
        Document.objects.create(
            household=h, client=c1, title='[DEMO] Investment Policy Statement',
            location='demo/ips.pdf'
        )
        return HttpResponse("Seeded demo. Visit /portal/household/1/")
    except Exception as e:
        import traceback
        return HttpResponse("SEED ERROR:<br><pre>" + traceback.format_exc() + "</pre>", status=500)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bootstrap", bootstrap),
    path("migrate", migrate_now),
    path("seed", seed),
    path("crm/", include("crm.urls")),
    path("portal/", include("portal.urls")),
    path("", home),
]
