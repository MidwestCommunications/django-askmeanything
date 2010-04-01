from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Sum

from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType

from authority.models import Permission

from models import Poll, Response, PublishedPoll
from forms import PollForm, AnswerFormSet, PublishFormSet
import poll_settings
from permissions import poll_permissions

def show(request, pollid):
    #this will be the src of a script tag
    poll = get_object_or_404(Poll, id=pollid)
    poll_form = render_to_string('poll_form.html', {'poll': poll})
    return render_to_response('poll.js', {'poll': poll, 'poll_form': poll_form}, mimetype='text/javascript')

def embed(request, pollid):
    #for embed in an iframe
    return render_to_response('poll_frame.html', {'poll_id': pollid})

@require_POST
def vote(request, pollid):
    #loaded by xmlhttprequest
    poll = get_object_or_404(Poll, id=pollid)
    
    try:
        selected_response = poll.responses.get(id=request.raw_post_data)
    except (KeyError, Response.DoesNotExist):
        #go directly to results without voting
        pass
    else:
        votedpolls = request.session.setdefault('votedpolls', [])
        if pollid not in votedpolls:
            request.session['votedpolls'].append(pollid)
            selected_response.votes += 1
            selected_response.save()
    
    return HttpResponseRedirect(reverse('askmeanything.views.results', kwargs={'pollid': pollid}))

def results(request, pollid):
    #loaded by xmlhttprequest
    poll = get_object_or_404(Poll, id=pollid)
    total_votes = float(poll.responses.aggregate(Sum('votes'))['votes__sum']) or 1.0
    poll_results = []
    for response in poll.responses.all():
        poll_results.append({
            'response': response,
            'percent': int(round(response.votes / total_votes * 100))
        })
    return render_to_response('poll_results.html', {'poll': poll, 'poll_results': poll_results}, mimetype='text/plain')

@permission_required('askmeanything.add_poll')
def new(request):
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        
        if poll_form.is_valid():
            new_poll = Poll.objects.create(question=poll_form.cleaned_data['question'], creator=request.user)
            
            answer_formset = AnswerFormSet(request.POST, instance=new_poll)
            if answer_formset.is_valid():
                answer_formset.save()
                return HttpResponseRedirect(reverse('askmeanything.views.publish', kwargs={'pollid': new_poll.id}))
            else:
                new_poll.delete()
    
    poll_form = PollForm()
    answer_formset = AnswerFormSet()
        
    return render_to_response('poll_create.html', {'poll_form': poll_form, 'answer_formset': answer_formset}, context_instance=RequestContext(request))

@permission_required('askmeanything.add_publishedpoll')
def publish(request, pollid):
    poll = get_object_or_404(Poll, id=pollid)
    
    if not poll.creator == request.user and not request.user.is_superuser:
        return HttpResponseForbidden('You cannot publish a poll that you did not create.')
    if not poll.open:
        raise Http404
    
    publish_done = False
    published_to = []
    if request.method == 'POST':
        publication_formset = PublishFormSet(request.POST)
        if publication_formset.is_valid():
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
                            #update published datetime
                            published_poll.save()
        publish_done = True
    
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
    
    publication_form_data = []
    publication_form_labels = []
    if allowed_publications:
        for item in allowed_publications:
            publication_type = ContentType.objects.get_for_model(item)
            publication_form_data.append({'publication_type_id': publication_type.id, 'publication_id': item.id})
            publication_form_labels.append(str(publication_type) + ' - ' + str(item))
        
    publication_formset = PublishFormSet(initial=publication_form_data)
    for i in xrange(len(publication_formset.forms)):
        publication_formset.forms[i].fields['publish'].label = publication_form_labels[i]
    
    return render_to_response('poll_publish.html', {'poll': poll, 'publish_done': publish_done, 'published_to': published_to, 'publication_formset': publication_formset}, context_instance=RequestContext(request))