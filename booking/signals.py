from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_migrate)
def create_user_roles(sender, **kwargs):
    # Create Groups
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    warden_group, _ = Group.objects.get_or_create(name='Warden')
    student_group, _ = Group.objects.get_or_create(name='Student')

    # Example permissions (you can create custom permissions in models if needed)
    # Assigning default Django permissions here as a demo
    # You can define more fine-grained permissions if required
    
    for group in [admin_group, warden_group, student_group]:
        group.permissions.clear()  # Optional: clear existing ones

    # Admin: full permissions
    admin_permissions = Permission.objects.all()
    admin_group.permissions.set(admin_permissions)

    # Warden: limited permissions (just for demo, adjust as needed)
    warden_permissions = Permission.objects.filter(codename__in=[
        'add_user', 'change_user', 'view_user',
    ])
    warden_group.permissions.set(warden_permissions)

    # Student: view only
    student_permissions = Permission.objects.filter(codename__in=[
        'view_user',
    ])
    student_group.permissions.set(student_permissions)
