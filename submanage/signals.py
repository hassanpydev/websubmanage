from django.db.models.signals import post_save, post_delete

from .models import Subdomain, Domain, Keyword
from .nginxHandler import create_new_site
from .worpress_poster import create_post
from .google_util.SeearchReults import get_search_results
from threading import Thread


def create_site(sender, instance, created, **kwargs):
    """
    Create profile when user is created
    """
    if created:
        site = instance
        create_new_site(site.get_full_domain())


def create_base_site(sender, instance, created, **kwargs):
    """
    Create profile when user is created
    """
    if created:
        site: Domain = instance
        create_new_site(site.name, base_domain=True)


def add_new_keyword(sender, instance, created, **kwargs):
    if created:
        keyword: Keyword = instance
        Thread(get_search_results(query_string=keyword.word, domain=keyword.subdomain.get_full_domain())).start()


def delete_site(sender, instance, **kwargs):
    """
    Delete user when profile is deleted
    """
    # todo delete site from database and nginx and directory in /var/www/html
    pass


post_save.connect(create_site, sender=Subdomain)
post_save.connect(add_new_keyword, sender=Keyword)
post_save.connect(create_base_site, sender=Domain)
post_delete.connect(delete_site, sender=Subdomain)
