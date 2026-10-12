# src/fraud_graph_explorer/graph_explorer/urls.py
from django.urls import path
from . import views

app_name = 'graph_explorer'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('ingest/', views.ingest_pdf_view, name='ingest_pdf'),
    path('ingest/confirm/', views.ingest_confirm_view, name='ingest_confirm'),
    path('cards/<uuid:sheet_id>/', views.app_cards_view, name='app_cards'),
    path('detail/<uuid:sheet_id>/', views.sheet_detail_view, name='sheet_detail'),
    path('delete/<uuid:sheet_id>/', views.delete_application_view, name='delete_application'),
    path('api/graph/<uuid:sheet_id>/', views.graph_data_view, name='graph_data'),
    path('api/icon/<str:entity_type>/', views._entity_icon_view, name='entity_icon'),
]