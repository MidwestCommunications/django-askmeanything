from operator import or_

from django.db import models

from django.contrib.auth.models import User

class Poll(models.Model):
    question = models.CharField(max_length=200)
    
    creator = models.ForeignKey(User, related_name='polls', editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __unicode__(self):
        return self.question
    
    @models.permalink
    def get_absolute_url(self):
        return ('askmeanything.views.show', (), {'poll_id': self.id})
    
    def get_script_tag(self):
        return '<script type="text/javascript" src="%sembed/"></script>' % \
            self.get_absolute_url()
    
    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'

class Response(models.Model):
    poll = models.ForeignKey(Poll, related_name='responses')
    answer = models.CharField(max_length=200)
    votes = models.IntegerField(default=0, editable=False)
    
    def __unicode__(self):
        return self.answer