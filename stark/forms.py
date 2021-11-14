from django import forms


class HomeForm(forms.Form):
    from_currency = forms.CharField()
    to_currency = forms.CharField()
