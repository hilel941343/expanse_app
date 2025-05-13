from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('add/', views.add_expense, name='add_expense'),
    path('summary/', views.summary, name='summary'),
    path('my/', views.my_expenses, name='my_expenses'),

]
