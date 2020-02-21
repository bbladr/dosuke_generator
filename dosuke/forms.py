from django import forms
from .models import Item, Event


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('name','age','sex','memo')
        widgets = {
                    'name': forms.TextInput(attrs={'placeholder':'ex：Taro Yamada'}),
                    'age': forms.NumberInput(attrs={'min':1}),
                    'sex': forms.RadioSelect(),
                    'memo': forms.Textarea(attrs={'rows':4}),
                  }

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name','band_list','memo')
        widgets = {
                    'name': forms.TextInput(attrs={'placeholder':'ex：Taro Yamada'}),
                    'band_list': forms.TextInput(attrs={'rows':4}),
                    'memo': forms.Textarea(attrs={'rows':4}),
                  }