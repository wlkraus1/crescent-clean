from django.urls import path
from django.http import HttpResponse

def home(_):
    return HttpResponse("CRM app is working.")

urlpatterns = [ path("", home, name="crm_home") ]
