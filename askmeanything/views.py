from django import forms
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseGone
from django.shortcuts import render_to_response
from django.conf import settings
from django.utils.encoding import smart_unicode
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType

from authority.models import Permission

from models import Poll, Response, PublishedPoll
from forms import PollForm, AnswerFormSet, PublishFormSet
import poll_settings
from permissions import poll_permissions

def show(request, pollid):
    #this might be AJAX only
    return HttpResponse("You're looking at poll %s." % pollid)

def results(request, pollid):
    #this will probably only be used for AJAX
    return HttpResponse("You're looking at the results of poll %s." % pollid)

def vote(request, pollid):
    return HttpResponse("You're voting on poll %s." % pollid)

@permission_required('askmeanything.add_poll')
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
    
    poll_form = PollForm()
    answer_formset = AnswerFormSet()
        
    return render_to_response('poll_create.html', {'poll_form': poll_form, 'answer_formset': answer_formset})

@permission_required('askmeanything.add_publishedpoll')
def publish(request, pollid):
    poll = Poll.objects.get(id=pollid)
    
    if not poll.creator == request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can only publish polls that you have created.")
    if not poll.open:
        return HttpResponseGone("This poll is closed and can no longer be published.")
    
    if request.method == 'POST':
        publication_formset = PublishFormSet(request.POST)
        if publication_formset.is_valid():
            published_to = []
            for cleaned_form_data in publication_formset.cleaned_data:
                if cleaned_form_data['publish']:
                    publication_type = ContentType.objects.get(id=cleaned_form_data['publication_type_id'])
                    publication_type_name = str(publication_type)
                    publication_id = cleaned_form_data['publication_id']
                    publication = publication_type.get_object_for_this_type(id=publication_id)
                    check = poll_permissions[publication_type_name](request.user)
                    if check.has_perm(publication_type_name + '_permission.publish_poll_' + publication_type_name, publication):
                        published_to.append(str(publication))
                        (published_poll, created) = PublishedPoll.objects.get_or_create(poll=poll, publication_type=publication_type, publication_id=publication_id)
                        if not created:
                            published_poll.save()
            if published_to:
                #success!
                return HttpResponse("You published poll %s." % pollid)
        return HttpResponse("The poll was not published.")
    
    allowed_publications = []
    for (app_name, model_name) in poll_settings.PUBLICATION_TYPES:
        publication_type = ContentType.objects.get(app_label=app_name, model=model_name)
        if request.user.is_superuser:
            allowed_publications.extend(publication_type.model_class().objects.all())
        elif request.user.is_active:
            publication_type_name = str(publication_type)
            perm_name = publication_type_name + '_permission.publish_poll_' + publication_type_name
            for publication_permission in Permission.objects.user_permissions(request.user, perm_name, publication_type.model_class()):
                allowed_publications.append(publication_permission.content_object)
    
    if allowed_publications:
        publication_form_data = []
        publication_form_labels = []
        for item in allowed_publications:
            publication_type = ContentType.objects.get_for_model(item)
            publication_form_data.append({'publication_type_id': publication_type.id, 'publication_id': item.id})
            publication_form_labels.append(str(publication_type) + ' - ' + str(item))
        publication_formset = PublishFormSet(initial=publication_form_data)
        for i in xrange(len(publication_formset.forms)):
            publication_formset.forms[i].fields['publish'].label = publication_form_labels[i]
        return render_to_response('poll_publish.html', {'publication_formset': publication_formset})
    return HttpResponseForbidden("You do not have permission to publish anywhere.")