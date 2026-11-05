# src/fraud_graph_explorer/graph_explorer/urls.py

# Fraud Graph Explorer
# Copyright (C) 2026 Luca Amodeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
    path('api/icon/<str:entity_type>/', views.entity_icon_view, name='entity_icon'),
]