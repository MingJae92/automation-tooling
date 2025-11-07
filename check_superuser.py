
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_app.settings')
django.setup()


superusers = User.objects.filter(is_superuser=True)
if superusers.exists():
    print("Superusers in the database:")
    for user in superusers:
        status = "active" if user.is_active else "inactive"
        print(f" - {user.username} ({status})")
else:
    print("No superusers found.")


username_to_test = input("Enter username to test: ")
password_to_test = input("Enter password to test: ")

user = authenticate(username=username_to_test, password=password_to_test)
if user:
    print(f"✅ Credentials for '{username_to_test}' are correct!")
else:
    print(f"❌ Invalid username or password for '{username_to_test}'")
