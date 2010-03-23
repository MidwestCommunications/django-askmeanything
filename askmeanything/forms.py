from django import forms
from django.forms.models import modelformset_factory
from models import Poll, Response

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('question',)

AnswerFormSet = modelformset_factory(Response, fields=('answer',), extra=5)
