import os
import sys
from getpass import getpass

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from django.contrib.auth import get_user_model


def main():
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin1234")

    User = get_user_model()
    user, created = User.objects.get_or_create(username=username, defaults={"email": email})
    if created:
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        print(f"Superuser created: {username} ({email})")
    else:
        # Update email and password to match request
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        print(f"Superuser updated: {username} ({email})")

    print("Credentials:")
    print("  username:", username)
    print("  email:", email)
    print("  password:", password)


if __name__ == "__main__":
    main()
