from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site

class Poll(models.Model):
    question = models.CharField(max_length=200)
    
    #want to restrict owner to be a user, group, or site
    OWNER_TYPE_CHOICES = setting.OWNER_TYPE_CHOICES or models.Q(app_label='auth', model='user') | models.Q(app_label='auth', model='group') | models.Q(app_label='sites', model='site')
    owner_type = models.ForeignKey(ContentType, limit_choices_to=OWNER_TYPE_CHOICES)
    owner_id = models.PositiveIntegerField()
    owner = generic.GenericForeignKey('owner_type', 'owner_id')
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __unicode__(self):
        return self.question
    
    class Meta:
        ordering = ['-created']

class ResponseChoice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
    
    def __unicode__(self):
        return self.choice
    
    class Meta:
        order_with_respect_to = 'poll'