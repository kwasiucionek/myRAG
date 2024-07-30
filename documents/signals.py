from django.db.models.signals import post_save
from django.contrib.auth.models import User, Permission
from django.dispatch import receiver

@receiver(post_save, sender=User)
def assign_permissions_to_all_users(sender, instance, created, **kwargs):
    if created:
        # Przypisanie uprawnienia do przeglądania dokumentów
        view_document_permission = Permission.objects.get(codename='view_document', content_type__app_label='documents')
        instance.user_permissions.add(view_document_permission)

        # Ustawienie statusu is_staff
        instance.is_staff = True

        # Zapisanie zmian w użytkowniku
        instance.save()
