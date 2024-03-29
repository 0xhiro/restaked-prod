from django import forms
from .models import UserEmail

class UserEmailForm(forms.ModelForm):
    class Meta:
        model = UserEmail
        fields = ['email']

class WalletAddressForm(forms.Form):
    wallet_address = forms.CharField(label='Wallet Address', max_length=42)