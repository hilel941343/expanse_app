from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    # Add more app-specific routes here
]
