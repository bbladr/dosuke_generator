from django import forms
from .models import Event

class EventForm(forms.ModelForm):

  class Meta:
    model = Event
    fields = ('name','band_list','memo')
    widgets = {
                'name': forms.TextInput(attrs={'placeholder':'イベント名'}),
                'band_list': forms.TextInput(attrs={'rows':4}),
                'memo': forms.Textarea(attrs={'rows':4}),
              }