from django import forms
from .models import Event

class EventForm(forms.ModelForm):

  class Meta:
    model = Event
    fields = ('name','memo')
    widgets = {
                'name': forms.TextInput(attrs={'placeholder':'イベント名'}),
                'memo': forms.Textarea(attrs={'rows':4}),
              }