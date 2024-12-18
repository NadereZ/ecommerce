from django import forms

class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3,
                                                           'placeholder': 'Enter your delivery address here: '}))