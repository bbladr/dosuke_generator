from django import forms

from .models import Band, Member, Config
from .functions import get_time_label

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

class ConfigForm(forms.Form):
  configs = {}
  for config in Config.objects.all():
    configs[config.key] = config.value

  time_choices = [(i, label) for i, label in enumerate(get_time_label())]
  sessionStart = forms.ChoiceField(
    label='セッション開始時間',
    widget=forms.Select,
    initial=[configs['session_start']],
    choices=time_choices,
    required=True,
  )
  sessionEnd = forms.ChoiceField(
    label='セッション終了時間',
    widget=forms.Select,
    initial=[configs['session_end']],
    choices=time_choices,
    required=True,
  )
  roomStart = forms.ChoiceField(
    label='防音室開始時間',
    widget=forms.Select,
    initial=[configs['room_start']],
    choices=time_choices,
    required=True,
  )
  roomEnd = forms.ChoiceField(
    label='防音室終了時間',
    widget=forms.Select,
    initial=[configs['room_end']],
    choices=time_choices,
    required=True,
  )

  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
          field.widget.attrs['class'] = 'form-control mb-3'

