from django import forms
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseGone
from django.shortcuts import render_to_response
from django.conf import settings
from django.utils.encoding import smart_unicode
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType

from models import Poll, Response, PublishedPoll
from forms import PollForm, AnswerFormSet, PublishForm
import poll_settings

def list(request):
    return HttpResponse("You're looking at a list of polls.")

def show(request, pollid):
    return HttpResponse("You're looking at poll %s." % pollid)

def results(request, pollid):
    return HttpResponse("You're looking at the results of poll %s." % pollid)

def vote(request, pollid):
    return HttpResponse("You're voting on poll %s." % pollid)

@permission_required('askmeanything.can_add_poll')
def new(request):
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        
        if poll_form.is_valid():
            new_poll = Poll(question=poll_form.cleaned_data['question'], creator=request.user)
            new_poll.save()
            
            answer_formset = AnswerFormSet(request.POST, instance=new_poll)
            if answer_formset.is_valid():
                answer_formset.save()
                return HttpResponseRedirect('../' + str(new_poll.id) + '/publish/')
            else:
                new_poll.delete()
    else:
        poll_form = PollForm()
        answer_formset = AnswerFormSet()
        
    return render_to_response('poll_create.html', {'poll_form': poll_form, 'answer_formset': answer_formset})

@permission_required('askmeanything.can_add_published_poll')
def publish(request, pollid):
    poll = Poll.objects.get(id=pollid)
    
    if not poll.creator == request.user:
        return HttpResponseForbidden("You can only publish polls that you have created.")
    if not poll.open:
        return HttpResponseGone("This poll is closed and can no longer be published.")
    
    #bad implementation! use formsets
    publication_forms = []
    for (app_name, model_name) in poll_settings.PUBLICATION_TYPES:
        publication_type = ContentType.objects.get(app_label=app_name, model=model_name)
        #does not incorporate publication permissions from authority
        for item in publication_type.model_class().objects.all():
            publish_form = PublishForm({'publication_type_id': publication_type.id, 'publication_id': item.id})
            if request.method == 'POST':
                publish_form = PublishForm(request.POST)
                if publish_form.is_valid():
                    (published_poll, created) = PublishedPoll.get_or_create(poll=poll, publication_type=publication_type, publication_id=item.id)
                    if not created:
                        published_poll.save()
            else:
                publish_form.fields['publish'].label = smart_unicode(str(publication_type) + ': ' + str(item))
                publication_forms.append(publish_form)
    return render_to_response('poll_publish.html', {'publication_forms': publication_forms})