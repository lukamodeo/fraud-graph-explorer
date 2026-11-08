# src/fraud_graph_explorer/graph_explorer/management/commands/bulk_ingest_pdfs.py

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
Bulk-ingest PDF loan applications from a folder.

Usage:
    python manage bulk_ingest_pdfs --folder /tmp/fraud_pdfs
    python manage bulk_ingest_pdfs --folder /tmp/fraud_pdfs --overwrite
"""
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from fraud_graph_explorer.graph_explorer.services import ingest_pdf


class Command(BaseCommand):
    help = "Bulk-ingest PDF loan applications from a folder."

    def add_arguments(self, parser):
        parser.add_argument('--user', type=str, required=True, help="Username to ingest the PDFs as (required)")
        parser.add_argument('--folder', type=str, required=True, help="Path to the folder containing PDF files")
        parser.add_argument('--overwrite', action='store_true', help="Overwrite existing sheets with the same request number")

    def handle(self, *args, **options):
        folder = options['folder']
        overwrite = options['overwrite']

        # ─── Validate user exists (graceful error, not a crash) ───
        try:
            user = User.objects.get(username=options['user'])
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f"User '{options['user']}' does not exist."
            ))
            available = list(User.objects.values_list('username', flat=True))
            if available:
                self.stdout.write(f"  Available users: {', '.join(available)}")
            else:
                self.stdout.write(f"  No users found. Create one with: manage createsuperuser")
            return

        if not os.path.isdir(folder):
            self.stdout.write(self.style.ERROR(f"Folder not found: {folder}"))
            return

        pdf_files = sorted(f for f in os.listdir(folder) if f.lower().endswith('.pdf'))

        if not pdf_files:
            self.stdout.write(self.style.WARNING(f"No PDF files in {folder}"))
            return

        self.stdout.write(f"Found {len(pdf_files)} PDFs | Overwrite: {overwrite}\n")

        success, duplicates, invalid, errors = 0, 0, 0, 0

        for filename in pdf_files:
            filepath = os.path.join(folder, filename)
            try:
                with open(filepath, 'rb') as f:
                    pdf_bytes = f.read()

                app, error_code, existing = ingest_pdf(
                    pdf_bytes=pdf_bytes,
                    file_name=filename,
                    overwrite=overwrite,
                    user=user,
                )

                if app:
                    self.stdout.write(self.style.SUCCESS(
                        f"  ✓ {filename} → {app.request_number} ({app.country_code})"
                    ))
                    success += 1
                elif error_code == 'duplicate':
                    self.stdout.write(self.style.WARNING(
                        f"  ⚠ {filename} → duplicate of {existing.request_number if existing else '?'}"
                    ))
                    duplicates += 1
                elif error_code == 'invalid_sheet':
                    self.stdout.write(self.style.ERROR(f"  ✗ {filename} → no recognizable fields"))
                    invalid += 1
                elif error_code == 'parse_error':
                    self.stdout.write(self.style.ERROR(f"  ✗ {filename} → parse error"))
                    errors += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ {filename} → {e}"))
                errors += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone: {success} ingested, {duplicates} duplicates, "
            f"{invalid} invalid, {errors} errors"
        ))