import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fraud_graph_explorer.graph_explorer.models import Application, Entity


class Command(BaseCommand):
    help = "Delete all applications (and associated PDFs) for a specific user."

    def add_arguments(self, parser):
        parser.add_argument('--user', type=str, required=True,
                            help="Username to clear data for")
        parser.add_argument('--clean-entities', action='store_true',
                            help="Also delete orphaned entities no longer referenced by any application")

    def handle(self, *args, **options):
        username = options['user']

        # ─── Validate user ───
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User '{username}' does not exist."))
            available = list(User.objects.values_list('username', flat=True))
            if available:
                self.stdout.write(f"  Available users: {', '.join(available)}")
            else:
                self.stdout.write("  No users found. Create one with: manage createsuperuser")
            return

        # ─── Get applications ───
        apps = Application.objects.filter(user=user)
        count = apps.count()

        if count == 0:
            self.stdout.write(self.style.WARNING(f"User '{username}' has no applications."))
            return

        # ─── Step 1: Collect file paths BEFORE deleting anything ───
        # Collect first so that if the DB delete fails, files are still on disk.
        pdf_paths = []
        for app in apps:
            if app.pdf_file:
                try:
                    pdf_paths.append(app.pdf_file.path)
                except (ValueError, NotImplementedError):
                    pass  # storage backend doesn't support .path

        # ─── Step 2: Delete DB records ───
        # If this fails, files are still on disk — no data loss, can retry.
        # Cascades to UsesIdentifier edges automatically.
        apps.delete()

        # ─── Step 3: Delete physical files (only reached if DB delete succeeded) ───
        deleted_pdfs = 0
        for file_path in pdf_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_pdfs += 1
            except OSError:
                pass  # file already gone or permission issue — skip

        self.stdout.write(self.style.SUCCESS(
            f"\nDeleted {count} applications for '{username}' "
            f"({deleted_pdfs} PDF files removed)."
        ))

        # ─── Optional: clean orphaned entities ───
        if options['clean_entities']:
            orphans = Entity.objects.filter(usesidentifier__isnull=True)
            orphan_count = orphans.count()
            orphans.delete()
            if orphan_count:
                self.stdout.write(self.style.SUCCESS(
                    f"Deleted {orphan_count} orphaned entities."
                ))