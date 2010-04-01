from operator import or_

from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

import poll_settings

class Poll(models.Model):
    question = models.CharField(max_length=200)
    
    creator = models.ForeignKey(User, related_name='polls', editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    open = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.question
    
    @models.permalink
    def get_absolute_url(self):
        return ('askmeanything.views.show', (), {'poll_id': self.id})
    
    def get_script_tag(self):
        return '<script type="text/javascript" src="' + self.get_absolute_url() + '"></script>'
    
    class Meta:
        ordering = ['-created']
        get_latest_by = ['created']

class Response(models.Model):
    poll = models.ForeignKey(Poll, related_name='responses')
    answer = models.CharField(max_length=200)
    votes = models.IntegerField(default=0, editable=False)
    
    def __unicode__(self):
        return self.answer

def get_publication_choices():   
    q_list = []
    for (app_name, model_name) in poll_settings.PUBLICATION_TYPES:
        q_list.append(models.Q(app_label=app_name, model=model_name))
    return reduce(or_, q_list)

class PublishedPoll(models.Model):
    poll = models.ForeignKey(Poll, related_name='publishings')
    
    publication_type = models.ForeignKey(ContentType, limit_choices_to=get_publication_choices())
    publication_id = models.PositiveIntegerField()
    publication = generic.GenericForeignKey('publication_type', 'publication_id')
    
    published = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return '"' + str(self.poll) + '" on ' + str(self.publication)
    
    class Meta:
        ordering = ['-published']
        get_latest_by = ['published']