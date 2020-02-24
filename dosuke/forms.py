from django import forms
from .models import Band, Member

class BandForm(forms.ModelForm):

  class Meta:
    model = Band
    fields = ('name','memo')
    widgets = {
                'name': forms.TextInput(attrs={'placeholder':'バンド名'}),
                'memo': forms.Textarea(attrs={'placeholder':'備考', 'rows':4}),
              }


class MemberForm(forms.ModelForm):

  class Meta:
    model = Member
    fields = ('name', 'entry_year', 'memo')
    widgets = {
                'name': forms.TextInput(attrs={'placeholder':'氏名'}),
                'entry_yaer': forms.NumberInput(),
                'memo': forms.Textarea(attrs={'placeholder':'備考', 'rows':4}),
              }