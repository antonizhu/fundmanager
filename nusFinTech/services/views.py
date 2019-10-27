from django.shortcuts import render
from django.http import HttpResponse
from services.forms import AccountTransactionForm
from services.models import Account, AccountTransaction, AccountSummary
from datetime import datetime
# Create your views here.

def index(request):
    dict = {'insert_here': 'starting point'}
    return render(request, 'index.html', context=dict)

def makeTransaction(request):
    accountTransactionForm = AccountTransactionForm()

    if request.method == 'POST':
        accountTxn = AccountTransaction(account = Account.objects.get(pk=1), dateTime = datetime.now()) #for now set all transaction to first user in db
        accountTransactionForm = AccountTransactionForm(request.POST, instance= accountTxn)
        if accountTransactionForm.is_valid():

            print("Amount: "+ str(accountTransactionForm.cleaned_data['amount']))
            accountTransactionForm.save()
        
        return index(request) #in the next step, may be redirect to report directly?
        
    return render(request, 'services/makeTransaction.html', {'form': accountTransactionForm})

def report(request):
    accountSummary = AccountSummary(account = Account.objects.get(pk=1))

    return render(request, 'services/report.html', {'ledger': accountSummary.transactionLedger})