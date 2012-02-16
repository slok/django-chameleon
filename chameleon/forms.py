from django import forms
import settings

choices=[('default', 'default'),]
for k, v in settings.CHAMELEON_SITE_THEMES.items():
    choices.append((k,k))


class ColorForm(forms.Form):
    theme = forms.ChoiceField( choices = choices,
                            widget=forms.Select(attrs={'onchange': 'this.form.submit();'}),
                            label='Select theme color',
                            required=True)
