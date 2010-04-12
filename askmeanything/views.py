from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Sum
from django.conf import settings

from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType

from models import Poll, Response
from forms import PollForm, AnswerFormSet

def show(request, poll_id):
    #mostly for embed in an iframe
    return render_to_response('poll_page.html', {'poll_id': poll_id})

def embed(request, poll_id):
    #this will be the src of a script tag
    poll = get_object_or_404(Poll, id=poll_id)
    poll_form = render_to_string('poll_form.html', {'poll': poll})
    return render_to_response('poll.js', {'poll': poll, 'poll_form': poll_form}, mimetype='text/javascript')

@require_POST
def vote(request, poll_id):
    #loaded by xmlhttprequest
    poll = get_object_or_404(Poll, id=poll_id)
    
    try:
        selected_response = poll.responses.get(id=request.raw_post_data)
    except (KeyError, Response.DoesNotExist):
        #go directly to results without voting
        pass
    else:
        votedpolls = request.session.setdefault('votedpolls', [])
        if poll_id not in votedpolls:
            request.session['votedpolls'].append(poll_id)
            request.session.modified = True
            selected_response.votes += 1
            selected_response.save()
    
    return HttpResponseRedirect(reverse('askmeanything.views.results', kwargs={'poll_id': poll_id}))

def results(request, poll_id):
    #loaded by xmlhttprequest
    poll = get_object_or_404(Poll, id=poll_id)
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
                redirect_to = getattr(settings, 'ASKMEANYTHING_NEW_REDIRECT', new_poll)
                return redirect(new_poll)
            else:
                new_poll.delete()
    
    poll_form = PollForm()
    answer_formset = AnswerFormSet()
    
    return render_to_response('poll_create.html', {'poll_form': poll_form, 'answer_formset': answer_formset}, context_instance=RequestContext(request))