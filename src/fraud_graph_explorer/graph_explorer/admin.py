# src/fraud_graph_explorer/graph_explorer/admin.py

from django.contrib import admin
from .models import Application, Entity, UsesIdentifier, Blacklist

@admin.register(Blacklist)
class BlacklistAdmin(admin.ModelAdmin):
    list_display = ('entity_type', 'value', 'reason', 'created_at')
    search_fields = ('value',)