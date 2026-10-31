# src/fraud_graph_explorer/sheet_crafter/urls.py

from django.urls import path
from . import views

app_name = 'sheet_crafter'

urlpatterns = [
    path('', views.sheet_crafter_view, name='crafter'),
    path('tins/', views.calculate_tin_view, name='calculate_tin'),
    path('generate-field/', views.generate_field_value, name='generate_field'),
]