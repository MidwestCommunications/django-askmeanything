from django import forms
from django.forms.models import modelformset_factory, inlineformset_factory
from models import Poll, Response

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('owner', 'question',)

ResponseFormSet = inlineformset_factory(
    Poll,
    Response,
    fields=('poll', 'answer'),
    extra=5,
    can_delete=False
)

class AnswerFormSet(ResponseFormSet):
    poll = forms.IntegerField(widget=forms.HiddenInput)

