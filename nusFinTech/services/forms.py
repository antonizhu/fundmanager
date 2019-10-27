from django import forms
from services.models import Account, AccountTransaction

class AccountTransactionForm(forms.ModelForm):
    class Meta:
        model = AccountTransaction
        fields = ['amount',]