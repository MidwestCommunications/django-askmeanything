from django.conf import settings

#defaults to profile & site
default_list = []
profile_model = getattr(settings, 'AUTH_PROFILE_MODULE', None)
if profile_model:
    default_list.append(profile_model)
default_list.append('sites.site')
types_list = getattr(settings, 'POLL_PUBLICATION_TYPES', default_list)
#returns a list of tuples like (app_name, model_name)
PUBLICATION_TYPES = [tuple(pub_type.rsplit('.', 1)) for pub_type in types_list]