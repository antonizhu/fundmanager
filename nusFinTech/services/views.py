from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from services.forms import AccountTransactionForm, UserForm, AccountForm
from services.models import Account, AccountTransaction, AccountSummary, MonthlySummary
from datetime import datetime

from django.contrib.auth import get_user_model, get_user
User = get_user_model()
# Create your views here.

def index(request):
    dict = {'insert_here': 'starting point'}
    return render(request, 'index.html', context=dict)

@login_required
def makeTransaction(request):
    accountTransactionForm = AccountTransactionForm()

    if request.method == 'POST':
        accountTxn = AccountTransaction(account = Account.objects.get(user=request.user), dateTime=datetime.now(tz=timezone.utc))
        accountTransactionForm = AccountTransactionForm(request.POST, instance= accountTxn)
        if accountTransactionForm.is_valid():

            print("Amount: "+ str(accountTransactionForm.cleaned_data['amount']))
            accountTransactionForm.save()
        
        return index(request) #in the next step, may be redirect to report directly?
        
    return render(request, 'services/makeTransaction.html', {'form': accountTransactionForm})
    
@login_required
def withdraw(request):
    account = Account.objects.get(user=request.user)
    account_summary = AccountSummary(account=account)
    account_transaction_form = AccountTransactionForm()
    if request.method == 'POST':
        amount = request.POST.get('amount')
        print ("Amount submitted: {0}".format(str(amount)))
        account_txn = AccountTransaction(account=account, dateTime=datetime.now(tz=timezone.utc), type=AccountTransaction.TYPEWITHDRAW)
        account_transaction_form = AccountTransactionForm(request.POST, instance=account_txn)
        print("Something")
        if account_transaction_form.is_valid():
            print("Allow to transact? {0} {1} - {2}".format(str(account_transaction_form.cleaned_data['amount'] < account_summary.transactionLedger[-1].balance), str(account_transaction_form.cleaned_data['amount']), str(account_summary.transactionLedger[-1].balance)))
        
            if account_transaction_form.cleaned_data['amount'] < account_summary.transactionLedger[-1].balance:
                print("Withdrawal amount: {0} {1}".format(str(account_transaction_form.cleaned_data['amount']), account_txn.type))
                account_transaction_form.save()
                account_summary = AccountSummary(account=account)
            else:
                print("Withdrawal over limit!")

    return render(request, 'services/withdraw.html', { 'form': account_transaction_form,
                                                       'name': account.name,
                                                       'balance':  account_summary.transactionLedger[-1].balance})

@login_required
def report(request):
    accountSummary = AccountSummary(account=Account.objects.get(user=request.user))
    return render(request, 'services/report.html', {'ledger': accountSummary.transactionLedger})

@login_required
def monthlyReport(request):
    account = Account.objects.get(user=request.user)
    monthly_summaries = account.monthly_summary.order_by('month_year_date')
    for monthly in monthly_summaries:
        print(monthly)
    return render(request, 'services/monthlyReport.html', {'ledger' : monthly_summaries})

@login_required
def yearlyReport(request):
    account = Account.objects.get(user=request.user)
    yearly_summaries = account.yearly_summary.order_by('year_date')
    for yearly in yearly_summaries:
        print(yearly)
    return render(request, 'services/yearlyReport.html', {'ledger' : yearly_summaries})


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        account_form = AccountForm(data = request.POST)

        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            account = account_form.save(commit=False)
            account.user = user
            account.save()

            registered = True
        else:
            print(user_form.errors, account_form.errors)

    else:
        user_form = UserForm()
        account_form = AccountForm()


    return render(request, 'register.html', {
                            'user_form': user_form, 
                            'account_form': account_form, 
                            'registered': registered})

@login_required
def user_consent(request):
    print("Username : {0}".format(request.user.username))

    account = Account.objects.get(user=request.user)
    if request.method == 'POST' and request.POST.get('agree') == 'True':
        print("Consent value given by user True")

        account.consentGiven = True
        account.save()
        return render(request, 'services/survey.html')
    
    return render(request, 'services/consent.html', {'name': account.name})

        
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                account = Account.objects.get(user=user)
                print("Consent given {0}".format(account.consentGiven))

                if account.consentGiven == True:
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'services/consent.html', {'name': account.name})
            else:
                return HttpResponse('Account Not Active')

        else:
            print('Fail to login username {0}'.format(username))
            return HttpResponse("Invalid  login account!")
    else:
        return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'login.html')