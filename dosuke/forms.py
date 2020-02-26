from django import forms
from .models import Band, Member

class BandForm(forms.ModelForm):

  class Meta:
    model = Band
    fields = ('name', 'members', 'memo')
    widgets = {
                'name': forms.TextInput(attrs={'placeholder':'バンド名', 'class': 'form-control'}),
                'members': forms.SelectMultiple(attrs={'class': 'form-control'}),
                'memo': forms.Textarea(attrs={'placeholder':'備考', 'class': 'form-control', 'rows':4}),
              }


class MemberForm(forms.ModelForm):

  class Meta:
    model = Member
    fields = ('name', 'entry_year', 'memo')
    widgets = {
                'name': forms.TextInput(attrs={'placeholder':'氏名', 'class': 'form-control'}),
                'entry_yaer': forms.NumberInput(attrs={'class': 'form-control'}),
                'memo': forms.Textarea(attrs={'placeholder':'備考', 'class': 'form-control', 'rows':4}),
              }