from django.http import HttpResponse

def home(_):
    return HttpResponse("Client Portal is working.")
