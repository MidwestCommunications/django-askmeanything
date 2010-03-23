from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from models import Poll, Response
from forms import PollForm, AnswerFormSet

def list(request):
    return HttpResponse("You're looking at a list of polls.")

def show(request, pollid):
    return HttpResponse("You're looking at poll %s." % pollid)

def results(request, pollid):
    return HttpResponse("You're looking at the results of poll %s." % pollid)

def vote(request, pollid):
    return HttpResponse("You're voting on poll %s." % pollid)

@login_required
def new(request):
    owner_choices = []
    
    user_ct_id = ContentType.objects.get(app_label='auth', model='user').id
    owner_choices.append((str(user_ct_id) + ',' + str(request.user.id), 'User: ' + request.user.username))
    
    group_ct_id = ContentType.objects.get(app_label='auth', model='group').id
    for group in request.user.groups.all():
        owner_choices.append((str(group_ct_id) + ',' + str(group.id), 'Group: ' + group.name))
    
    site_ct_id = ContentType.objects.get(app_label='sites', model='site').id
    site = Site.objects.get_current()
    owner_choices.append((str(site_ct_id) + ',' + str(site.id), 'Site: ' + site.name))
    
    owner_form = forms.Form()
    owner_form.fields['owner'] = forms.ChoiceField(choices=owner_choices)
    poll_form = PollForm()
    answer_formset = AnswerFormSet(queryset=Response.objects.none())
    
    #this stuff is just for testing
    output = '<html><body><form><table>'
    output += str(owner_form) + str(poll_form) + str(answer_formset)
    output += '</table></form></html></body>'
    return HttpResponse(output)