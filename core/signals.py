from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.sites.models import Site

@receiver(post_migrate)
def setup_site(sender, **kwargs):
    site = Site.objects.get_or_create(id=1)[0]
    site.domain = '127.0.0.1:8000'
    site.name = 'TaleForge'
    site.save() 