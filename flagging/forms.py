from django import forms
from .models import Flag


class FlagForm(forms.ModelForm):
    class Meta:
        model = Flag
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe why you are flagging this event...'}),
        }