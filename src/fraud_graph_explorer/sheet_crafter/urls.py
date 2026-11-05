# src/fraud_graph_explorer/sheet_crafter/urls.py

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

app_name = 'sheet_crafter'

urlpatterns = [
    path('', views.sheet_crafter_view, name='crafter'),
    path('tins/', views.calculate_tin_view, name='calculate_tin'),
    path('generate-field/', views.generate_field_value, name='generate_field'),
]