# src/fraud_graph_explorer/config/urls.py

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

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView

from .views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    # ─── Auth routes ───
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Root → redirect to explorer (which redirects to login if not authenticated)
    path('', RedirectView.as_view(url='/explorer/')),

    # Apps
    path('crafter/', include('fraud_graph_explorer.sheet_crafter.urls')),
    path('explorer/', include('fraud_graph_explorer.graph_explorer.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
