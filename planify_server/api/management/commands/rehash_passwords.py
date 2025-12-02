from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from api.models import User

class Command(BaseCommand):
    help = "Re-hash passwords of users that still have plaintext passwords."

    def handle(self, *args, **options):
        users = User.objects.all()
        fixed= 0

        for u in users:
            pw = u.password

            if "$" not in pw:
                self.stdout.write(self.style.WARNING(f"Rehashing password for {u.email}"))
                u.password = make_password(pw)
                u.save(update_fields=["password"])
                fixed +=1
            else:
                self.stdout.write(f"OK → already hashed: {u.email}")

        self.stdout.write(self.style.SUCCESS(f"Done. {fixed} passwords rehashed."))
