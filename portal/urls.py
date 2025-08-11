from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="portal_home"),
    path("household/<int:pk>/", views.household_view, name="portal_household"),
]
