from django import forms
import settings

choices=[]
for k, v in settings.CHAMELEON_SITE_THEMES.items():
    choices.append((k,k))


class ColorForm(forms.Form):
    theme = forms.ChoiceField( choices = choices,
                            widget=forms.Select(),
                            label='Select the3me color',
                            required=True)
