# src/fraud_graph_explorer/graph_explorer/management/commands/bulk_generate_pdfs.py

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

"""
Bulk-generate synthetic PDF loan applications with optional country mixing.

Usage:
    python manage bulk_generate_pdfs --count 50 --output-dir /tmp/pdfs
    python manage bulk_generate_pdfs --count 100 --mixing
    python manage bulk_generate_pdfs --count 20 --mixing --mixing-probability 0.3
"""

import os
import random
from django.core.management.base import BaseCommand

from fraud_graph_explorer.domain_schema import FIELDS, CountryCodes
from fraud_graph_explorer.sheet_crafter.services import (
    generate_dynamic_initial_data,
    generate_pdf_sheet,
    get_calculated_tin,
)
from fraud_graph_explorer.sheet_crafter.seed_data import (
    get_random_data,
    get_random_profile,
)


def _apply_mixing(data, sheet_country, probability):
    """Randomly override VAT/TIN/IBAN fields with foreign country values."""
    country_codes = [c.value for c in CountryCodes]
    other_countries = [c for c in country_codes if c != sheet_country]

    for internal_name, config in FIELDS.items():
        tags = config.get('tags', [])
        if not any(t in tags for t in ('VAT', 'TIN', 'IBAN')):
            continue
        if random.random() > probability:
            continue

        override_country = random.choice(other_countries)

        if 'VAT' in tags:
            data[internal_name] = get_random_data(override_country, 'vat')
        elif 'IBAN' in tags:
            data[internal_name] = get_random_data(override_country, 'iban')
        elif 'TIN' in tags:
            calc_fields = config.get('calc_fields', {})
            if override_country in ('IT', 'FR'):
                data[internal_name] = get_calculated_tin(override_country, {
                    'fullname': data.get(calc_fields.get('fullname', ''), ''),
                    'sex': data.get(calc_fields.get('sex', ''), '') or 'M',
                    'dob': data.get(calc_fields.get('dob', ''), ''),
                    'birthplace': data.get(calc_fields.get('birthplace', ''), ''),
                    })
            else:
                data[internal_name] = get_random_profile(override_country)['tin']

    return data


def _inject_typo(value):
    """
    Inject a single random typo into an identifier value.
    Preserves the first 2 chars (country prefix for VAT/IBAN) so the
    identifier is still recognizable as a specific country's format,
    but has an invalid checksum/format.

    Returns the typo'd value, or the original if too short to typo.
    """
    if not value or len(value) < 4:
        return value

    # Typo type: substitute, delete, or insert
    typo_type = random.choice(['substitute', 'delete', 'insert'])

    if typo_type == 'substitute':
        # Replace one char (after the country prefix)
        pos = random.randint(2, len(value) - 1)
        original = value[pos]
        if original.isdigit():
            new_char = random.choice('0123456789'.replace(original, ''))
        else:
            new_char = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.replace(original.upper(), ''))
        return value[:pos] + new_char + value[pos + 1:]

    elif typo_type == 'delete':
        # Delete one char (after the country prefix)
        pos = random.randint(2, len(value) - 1)
        return value[:pos] + value[pos + 1:]

    elif typo_type == 'insert':
        # Insert one random char (after the country prefix)
        pos = random.randint(2, len(value))
        if value[-1].isdigit():
            new_char = random.choice('0123456789')
        else:
            new_char = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        return value[:pos] + new_char + value[pos:]

    return value


class Command(BaseCommand):
    help = "Bulk-generate synthetic PDF loan applications with optional country mixing and typos."

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10,
                            help="Number of PDFs to generate (default: 10)")

        parser.add_argument('--output-dir', type=str, default='/tmp/seed',
                            help="Output directory (default: /tmp/seed)")

        parser.add_argument('--mixing', action='store_true',
                            help="Enable random country mixing for VAT/TIN/IBAN fields")

        parser.add_argument('--mixing-probability', type=float, default=0.2,
                            help="Probability per VAT/TIN/IBAN field to override country (default: 0.2 = 20%%)")

        parser.add_argument('--typo', action='store_true',
                            help="Enable typo injection for VAT/TIN/IBAN fields")

        parser.add_argument('--typo-probability', type=float, default=0.1,
                            help="Probability per PDF to inject a typo in a random VAT/TIN/IBAN field (default: 0.1 = 10%%)")

    def handle(self, *args, **options):
        count = options['count']
        output_dir = options['output_dir']
        mixing = options['mixing']
        mixing_prob = options['mixing_probability']
        typo = options['typo']
        typo_prob = options['typo_probability']

        os.makedirs(output_dir, exist_ok=True)
        country_codes = [c.value for c in CountryCodes]

        success, failed = 0, 0

        for i in range(count):
            typo_info = ""
            sheet_country = random.choice(country_codes)
            data = generate_dynamic_initial_data(sheet_country)

            if mixing:
                data = self._apply_mixing(data, sheet_country, mixing_prob)

            if typo and typo_prob > 0 and random.random() < typo_prob:
                # Pick a random identifier field to typo
                identifier_fields = [f for f, c in FIELDS.items()
                                     if any(t in c.get('tags', []) for t in ('VAT', 'TIN', 'IBAN'))
                                     and f in data]  # only fields that exist in this form

                if identifier_fields:
                    field_to_typo = random.choice(identifier_fields)
                    original_value = data[field_to_typo]
                    data[field_to_typo] = _inject_typo(original_value)
                    typo_info = f"  → typo injected in {field_to_typo}: '{original_value}' → '{data[field_to_typo]}'"

            req_num = data.get('request_number', f'APP-{i:04d}')
            safe = "".join(c for c in req_num if c.isalnum() or c in '-_').rstrip()
            filepath = os.path.join(output_dir, f"{safe}.pdf")

            try:
                generate_pdf_sheet(sheet_country, data, filepath)
                self.stdout.write(f"  ✓ {safe}.pdf ({sheet_country}) {typo_info}")
                success += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ {safe}.pdf — {e}"))
                failed += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone: {success} generated, {failed} failed → {output_dir}"
        ))

