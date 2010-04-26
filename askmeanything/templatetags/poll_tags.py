from django import template
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User

from askmeanything.models import Poll

register = template.Library()

@register.tag
def show_poll(parser, token):
    try:
        (tag_name, poll_variable) = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return PollFormNode(poll_variable)

class PollFormNode(template.Node):
    def __init__(self, poll_variable_name):
        self.poll_variable = template.Variable(poll_variable_name)
    
    def render(self, context):
        try:
            poll = self.poll_variable.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        if not isinstance(poll, Poll):
            try:
                poll = Poll.objects.get(id=int(poll))
            except Poll.DoesNotExist:
                return ''
        return poll.get_script_tag()

@register.tag
def get_last_poll_for_user(parser, token):
    try:
        (tag_name, user_variable) = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return LatestPollNode(user_variable)

class LatestPollNode(template.Node):
    def __init__(self, user_variable_name):
        self.user_variable = template.Variable(user_variable_name)
    
    def render(self, context):
        try:
            user = self.user_variable.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        if not isinstance(user, User):
            try:
                user = User.objects.get(id=int(user))
            except TypeError, User.DoesNotExist:
                return ''
        try:
            last_poll = Poll.objects.filter(creator=user).latest()
        except Poll.DoesNotExist:
            return ''
        context['last_poll'] = last_poll
        return ''
