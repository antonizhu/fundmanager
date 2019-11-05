from django import forms
from django.contrib.auth.models import User
from services.models import Account, AccountTransaction

class AccountTransactionForm(forms.ModelForm):
    class Meta():
        model = AccountTransaction
        fields = ['amount',]

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ['username', 'email', 'password',]

class AccountForm(forms.ModelForm):
    class Meta():
        model = Account
        fields = ['name', 'mobileNo',]

class AccountETFForm(forms.ModelForm):
    class Meta():
        model = Account
        fields = ['selectedETF',]