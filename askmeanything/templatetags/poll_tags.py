from django import template
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.contenttypes.models import ContentType

from askmeanything.models import Poll, PublishedPoll

register = template.Library()

@register.tag
def show_latest_poll_for(parser, token):
    try:
        (tag_name, publication_variable_name) = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return PublishedPollFormNode(publication_variable_name)

class PublishedPollFormNode(template.Node):
    def __init__(self, publication_variable_name):
        self.publication_variable = template.Variable(publication_variable_name)
    
    def render(self, context):
        try:
            publication = self.publication_variable.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        publication_type = ContentType.objects.get_for_model(publication)
        try:
            poll = PublishedPoll.objects.filter(publication_type=publication_type, publication_id=publication.id).latest().poll
        except ObjectDoesNotExist:
            return ''
        return '<script type="text/javascript" src="' + poll.get_absolute_url + '"></script>'

@register.tag
def show_poll(parser, token):
    try:
        (tag_name, poll_id) = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return PollFormNode(poll_id)

class PollFormNode(template.Node):
    def __init__(self, poll_id):
        self.poll_id = poll_id
    
    def render(self, context):
        try:
            poll = Poll.objects.filter(id=self.poll_id)
        except ObjectDoesNotExist:
            return ''
        return '<script type="text/javascript" src="' + poll.get_absolute_url + '"></script>'