from django import forms
from .models import Band, Member

class BandForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
          field.widget.attrs['class'] = 'form-control'
          
  class Meta:
    model = Band
    fields = ('name', 'members', 'memo')
    widgets = {
                'name': forms.TextInput(attrs={'placeholder':'バンド名'}),
                'members': forms.SelectMultiple(),
                'memo': forms.Textarea(attrs={'placeholder':'備考', 'rows':4}),
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