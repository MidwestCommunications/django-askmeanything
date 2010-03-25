from django.conf import settings
from django.contrib.sites.models import Site

import authority
from authority import permissions

class SitePermission(permissions.BasePermission):
    label = 'site_permission'
    checks = ('publish_poll',)

authority.register(Site, SitePermission)