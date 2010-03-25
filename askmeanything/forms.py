from django import forms
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory

from models import Poll, Response, PublishedPoll

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('question',)

ResponseFormSet = inlineformset_factory(Poll, Response, fields=('poll', 'answer'), extra=5, can_delete=False)
class AnswerFormSet(ResponseFormSet):
    poll = forms.IntegerField(widget=forms.HiddenInput)

class PublishForm(forms.Form):
    publication_type_id = forms.IntegerField(widget=forms.HiddenInput)
    publication_id = forms.IntegerField(widget=forms.HiddenInput)
    publish = forms.BooleanField(required=False)

PublishFormSet = formset_factory(PublishForm, extra=0)