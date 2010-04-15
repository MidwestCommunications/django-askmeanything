from django import forms
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory

from models import Poll, Response

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('question',)

ResponseFormSet = inlineformset_factory(Poll, Response, fields=('poll', 'answer'), extra=5, can_delete=False)
class AnswerFormSet(ResponseFormSet):
    poll = forms.IntegerField(widget=forms.HiddenInput)
    def _get_media(self):
        return forms.Media(js=('askmeanything/pollresponsesform.js',))
    media = property(_get_media)