from django import template
from django.core.exceptions import ObjectDoesNotExist

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
            except TypeError, ObjectDoesNotExist:
                return ''
        return poll.get_script_tag()
