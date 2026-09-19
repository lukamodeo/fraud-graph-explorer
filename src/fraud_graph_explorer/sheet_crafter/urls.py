# src/fraud_graph_explorer/sheet_crafter/urls.py
from django.urls import path
from . import views

app_name = 'sheet_crafter'

urlpatterns = [
    path('', views.sheet_crafter_view, name='crafter'),
    path('tax-codes/', views.calculate_tax_code_view, name='calculate_tax_code'),
]