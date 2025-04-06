import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaleForge.settings')
django.setup()

from django.contrib.sites.models import Site

def setup_site():
    site = Site.objects.get_or_create(id=1)[0]
    site.domain = '127.0.0.1:8000'
    site.name = 'TaleForge'
    site.save()
    print('Site configuration updated successfully!')

if __name__ == '__main__':
    setup_site() 