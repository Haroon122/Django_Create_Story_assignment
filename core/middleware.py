from django.contrib.sites.models import Site
from django.conf import settings

class SiteSetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ensure site is configured
        site = Site.objects.get_or_create(id=settings.SITE_ID)[0]
        if site.domain != settings.SITE_DOMAIN or site.name != settings.SITE_NAME:
            site.domain = settings.SITE_DOMAIN
            site.name = settings.SITE_NAME
            site.save()
        
        response = self.get_response(request)
        return response 