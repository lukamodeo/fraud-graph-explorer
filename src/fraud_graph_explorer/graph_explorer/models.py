# src/fraud_graph_explorer/graph_explorer/models.py

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

import uuid

from django.db import models
from django.conf import settings

from fraud_graph_explorer.domain_schema import FIELDS, EntityTypes, CountryCodes


def pdf_upload_path(instance, filename):
    return f'pdfs/{instance.country_code}/{filename}'


class Blacklist(models.Model):
    """
    Stores blacklisted identifiers (VATs, TINs, IBANs, IPs) dynamically.
    """
    class EntityTypes(models.TextChoices):
        VAT = 'VAT', 'VAT Number'
        TIN = 'TIN', 'Tax ID Number'
        IBAN = 'IBAN', 'IBAN Code'
        IP = 'IP', 'IP Address'
        EMAIL = 'EMAIL', 'Email Address'

    entity_type = models.CharField(max_length=10, choices=EntityTypes.choices)
    value = models.CharField(max_length=255, help_text="The normalized identifier (e.g., IT04149371009)")
    reason = models.CharField(max_length=255, blank=True, null=True, help_text="Why is this blacklisted?")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()  # explicitly add manager

    class Meta:
        unique_together = ('entity_type', 'value')

    def __str__(self):
        return f"[{self.entity_type}] {self.value}"


class Application(models.Model):
    """
    Represents a single Bank Loan Application PDF (A 'Sheet' Vertex).
    """

    # Primary Key
    sheet_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    # Fixed Metadata
    file_name = models.CharField(max_length=255, blank=True, null=True)
    acquisition_date = models.DateTimeField(auto_now_add=True)

    # Booleans for fast HTMX list filtering
    has_validation_errors = models.BooleanField(default=False)
    has_rule_warnings = models.BooleanField(default=False)

    # Stores the original raw text from the PDF for any Sheet-typed field.
    # Used by sheet_detail_view for forensic-grade display
    # (preserves currency symbols, separators, exact formatting from the source PDF).
    # The typed columns (request_amount DecimalField, etc.) are still used for filtering and validation.
    raw_data = models.JSONField(default=dict, blank=True)

    # JSON Fields for detailed UI display
    validation_errors = models.JSONField(default=list, blank=True)
    rule_warnings = models.JSONField(default=list, blank=True)

    country_code = models.CharField(max_length=2, choices=CountryCodes.choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    pdf_file = models.FileField(upload_to=pdf_upload_path, blank=True, null=True)

    # Type hint for PyCharm to understand the reverse M2M relation
    entities: 'models.Manager[Entity]'

    objects = models.Manager()  # explicitly add manager

    def __str__(self):
        return f"Sheet {self.sheet_id} - {self.file_name}"

    def get_entity(self, entity_type):
        entity = self.entities.filter(entity_type=entity_type).first()
        return entity.value if entity else "N/A"


# Dynamically add fields to Application based on domain_schema.py
for internal_name, config in FIELDS.items():
    # Only add fields tagged as "Sheet" and not hidden
    if "Sheet" in config.get("tags", []) and not config.get("hidden"):
        field_type = config.get("type", "string")
        max_len = config.get("max_length", 255)

        if field_type in ["string", "keyword", "text"]:
            Application.add_to_class(
                internal_name,
                models.CharField(max_length=max_len, blank=True, null=True)
            )
        elif field_type == "decimal":
            Application.add_to_class(
                internal_name,
                models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
            )
        elif field_type == "date":
            Application.add_to_class(
                internal_name,
                models.DateField(blank=True, null=True)
            )




class Entity(models.Model):
    """
    Represents an Identifier (A connecting Vertex in the graph).
    """
    entity_type = models.CharField(
        max_length=20,
        choices=EntityTypes.choices,
        db_index=True,
    )

    value = models.CharField(max_length=100, db_index=True)


    # ─── Country the identifier's format belongs to ───
    # For VAT/TIN: populated by detect_vat_country() / detect_tin_country()
    #              at ingest time (only if valid VAT/TIN).
    # For other types (FULLNAME, IBAN, IP, EMAIL, PHONE, COMPANY, LOCATION):
    #              the format doesn't carry country info, so this stays NULL.
    country_code = models.CharField(
        max_length=2,
        db_index=True,
        null=True,
        blank=True,
        help_text=(
            "ISO 3166-1 alpha-2 code of the country whose format "
            "validates this identifier value (IT, DE, FR, ES, GB). "
            "NULL means either: (a) the entity type has no country-aware "
            "format (FULLNAME, IP, EMAIL, etc.) OR (b) the value is "
            "invalid for all 5 target countries — see validation_errors."
        ),
    )

    applications = models.ManyToManyField(Application, through='UsesIdentifier', related_name='entities')

    objects = models.Manager()  # explicitly add manager

    class Meta:
        unique_together = ('entity_type', 'value')   # unchanged

        # ─── CheckConstraint REMOVED ───
        # The original constraint required country_code NOT NULL for
        # VAT/TIN entities, but this conflicted with the requirement to
        # save invalid identifiers for forensic evidence and PDF
        # reconstruction. NULL now means "country unknown" (invalid
        # value or non-country-aware type), which is informative on
        # its own. The ingest pipeline (services.ingest_pdf) populates
        # country_code at creation time when detection succeeds.
        # ────────────────────────────────

    def __str__(self):
        # noinspection PyUnresolvedReferences
        label = self.get_entity_type_display()
        if self.country_code:
            return f"{label}: {self.value} ({self.country_code})"
        return f"{label}: {self.value}"

class UsesIdentifier(models.Model):
    """
    The Edge connecting a Sheet to an Identifier.
    """
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    source_field = models.CharField(max_length=100, blank=True, null=True)  # e.g., "company_vat"

    # Forensic record of exactly what was extracted from the PDF (only stripped)
    original_value = models.CharField(max_length=255, blank=True, null=True)

    objects = models.Manager()  # explicitly add manager

    class Meta:
        # ADDED source_field! An app can link to the same entity multiple times
        # as long as it comes from different fields on the PDF.
        unique_together = ('application', 'entity', 'source_field')

