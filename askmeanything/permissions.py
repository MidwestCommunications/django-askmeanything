from django.contrib.contenttypes.models import ContentType

import authority
from authority.permissions import BasePermission

from poll_settings import PUBLICATION_TYPES

def poll_permission_factory(object_model):
    permission_class_name = object_model.__name__ + 'Permission'
    permission_dict = {
        'label': object_model.__name__.lower() + '_permission',
        'checks': ('publish_poll',)
    }
    return type(permission_class_name, (BasePermission,), permission_dict)

poll_permissions = {}
for (app_name, model_name) in PUBLICATION_TYPES:
    object_model = ContentType.objects.get(app_label=app_name, model=model_name).model_class()
    poll_permissions[model_name] = poll_permission_factory(object_model)
    authority.register(object_model, poll_permissions[model_name])