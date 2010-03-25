from operator import or_
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site

class Poll(models.Model):
    question = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    
    open = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.question
    
    class Meta:
        ordering = ['-created']
        get_latest_by = ['created']

class Response(models.Model):
    poll = models.ForeignKey(Poll)
    answer = models.CharField(max_length=200)
    votes = models.IntegerField(default=0, editable=False)
    
    def __unicode__(self):
        return self.answer

def get_publication_choices():
    """looks for POLL_PUBLICATION_TYPES in settings, defaults to profile & site"""
    default_list = []
    profile = getattr(settings, 'AUTH_PROFILE_MODULE', None)
    if profile:
        default_list.append(profile)
    default_list.append('sites.site')
    
    app_model_list = getattr(settings, 'POLL_PUBLICATION_TYPES', default_list)
    q_list = []
    for app_model in app_model_list:
        (app_name, model_name) = app_model.rsplit('.', 1)
        q_list.append(models.Q(app_label=app_name, model=model_name))
    return reduce(or_, q_list)

class PublishedPoll(models.Model):
    poll = models.ForeignKey(Poll)
    
    publication_type = models.ForeignKey(ContentType, limit_choices_to=get_publication_choices())
    publication_id = models.PositiveIntegerField()
    publication = generic.GenericForeignKey('publication_type', 'publication_id')
    
    published = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __unicode__(self):
        return '"' + str(self.poll) + '" on ' + str(publication)
    
    class Meta:
        ordering = ['-published']
        get_latest_by = ['published']