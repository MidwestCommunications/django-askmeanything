from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms

from django.contrib.auth.decorators import login_required, permission_required
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
#@permission_required('askmeanything.
def new(request, pollid=None):
    owner_choices = []
    
    user_ct_id = ContentType.objects.get(app_label='auth', model='user').id
    owner_choices.append((str(user_ct_id) + ' ' + str(request.user.id), 'User: ' + request.user.username))
    
    group_ct_id = ContentType.objects.get(app_label='auth', model='group').id
    for group in request.user.groups.all():
        owner_choices.append((str(group_ct_id) + ' ' + str(group.id), 'Group: ' + group.name))
    
    site_ct_id = ContentType.objects.get(app_label='sites', model='site').id
    site = Site.objects.get_current()
    owner_choices.append((str(site_ct_id) + ' ' + str(site.id), 'Site: ' + site.name))
    
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        poll_form.fields['owner'] = forms.ChoiceField(choices=owner_choices)
        
        if poll_form.is_valid():
            (owner_ct_id, owner_id) = poll_form.cleaned_data['owner'].split()
            owner_object = ContentType.objects.get(id=owner_ct_id).get_object_for_this_type(id=owner_id)
            new_poll = Poll(question=poll_form.cleaned_data['question'], owner=owner_object)
            new_poll.save()
            
            answer_formset = AnswerFormSet(request.POST, instance=new_poll)
            if answer_formset.is_valid():
                answer_formset.save()
                return HttpResponseRedirect('../' + str(new_poll.id) + '/')
            else:
                new_poll.delete()
    else:
        poll_form = PollForm()
        poll_form.fields['owner'] = forms.ChoiceField(choices=owner_choices)
        answer_formset = AnswerFormSet()
        
    return render_to_response('poll_create.html', {'poll_form': poll_form, 'answer_formset': answer_formset})