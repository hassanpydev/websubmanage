from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Subdomain
from .nginxHandler import create_new_site


def create_site(sender, instance, created, **kwargs):
    """
    Create profile when user is created
    """
    if created:
        site = instance
        create_new_site(site.get_full_domain())


def delete_site(sender, instance, **kwargs):
    """
    Delete user when profile is deleted
    """
    # todo delete site from database and nginx and directory in /var/www/html
    pass


post_save.connect(create_site, sender=Subdomain)
post_delete.connect(delete_site, sender=Subdomain)
