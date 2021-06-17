from django import forms


class ReportsSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        fields = ('search', 'date_from', 'date_to')
