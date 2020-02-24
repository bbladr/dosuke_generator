from django import forms
from .models import Event, Band, Member

class EventForm(forms.ModelForm):

  class Meta:
    model = Event
    fields = ('name','memo')
    widgets = {
                'name': forms.TextInput(attrs={'placeholder':'イベント名'}),
                'memo': forms.Textarea(attrs={'rows':4}),
              }


class BandForm(forms.ModelForm):

  class Meta:
    model = Band
    fields = ('name','memo')
    widgets = {
                'name': forms.TextInput(attrs={'placeholder':'バンド名'}),
                'memo': forms.Textarea(attrs={'rows':4}),
              }


class MemberForm(forms.ModelForm):

  class Meta:
    model = Member
    fields = ('name', 'entry_year', 'memo')
    widgets = {
                'name': forms.TextInput(attrs={'placeholder':'氏名'}),
                'entry_yaer': forms.NumberInput(),
                'memo': forms.Textarea(attrs={'rows':4}),
              }