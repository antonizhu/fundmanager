import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','nusFinTech.settings')

import django
django.setup()


import random
from services.models import ETF, ETFHistory, Account, AccountTransaction
from faker import Faker
from datetime import datetime
from datetime import timedelta
fakegen = Faker()
nDays = 20

def generateETFs():

    etfList = []
    etfs = ['Low_Risk', 'Medium_Risk', 'High_Risk']
    for etf in etfs:
        print('getting or creating {0}'.format(etf))
        etfObj = ETF.objects.get_or_create(name=etf)[0]
        
        etfList.append(etfObj)

    for etfObj in etfList:
        print(etfObj)
        
    return etfList

def generateETFHistories(etfs):

    startDate = datetime.now().date() - timedelta(days= nDays)

    riskLevel = 0
    for etf in etfs:
        riskLevel += 1
        for aDate in (startDate + timedelta(days= n) for n in range(nDays+1)):
            delta = riskLevel * random.randint(-10,10)/1000
            etfHistory = ETFHistory.objects.get_or_create(etf= etf, date= aDate, delta= delta)[0]
            etfHistory.save()

def generateAccounts(etfs):
    accounts = []
    accountsDict = [{'name': 'Jing Xia','mobileNo': '83999123', 'selectedETF': etfs[0]},
        #{'name': 'Katy Parrot','mobileNo': '83666384', 'selectedETF': etfs[1]},
        #{'name': 'Kaley Coco','mobileNo': '83555384', 'selectedETF': etfs[2]},
    ]
    for accountDict in accountsDict:
        account = Account.objects.get_or_create(name=accountDict['name'], mobileNo= accountDict['mobileNo'], selectedETF = accountDict['selectedETF'])[0]
        accounts.append(account)

    for account in accounts:
        print(account)
    return accounts

def generateAccountTransaction(accounts):

    startDate = datetime.now() - timedelta(days= nDays)
    for account in accounts:
        for aDate in (startDate + timedelta(days= n) for n in range(nDays+1)):
            aDate = aDate.replace(hour= random.randint(9,15))

            amount = round((0.1 + random.random()) % 1.0, 2)
            AccountTransaction.objects.get_or_create(account = account, amount = amount, dateTime = aDate)

def generateProfitAccountTransaction(accounts):
    for account in accounts:
        balance = 0
        #get accountTransaction order by date
        #iterate trxn
        # balance += trxn.amount
        # find etf delta for the date
        account_transaction = account.transactions.order_by('dateTime')
        history = account.selectedETF.history.order_by('date')
        balance = 0
        for txn in account_transaction:
            balance += txn.amount
            etf_delta = {h for h in history if h.date == txn.dateTime.date()}
            
            amount = balance * etf_delta.pop().delta
            transaction_type = AccountTransaction.TYPEPROFIT
            if amount < 0 : 
                transaction_type = AccountTransaction.TYPELOSS
                amount = abs(amount)
            date = txn.dateTime
            date = date.replace(hour=23, minute=59, second=59)
            print('{0} {1} {2} {3}'.format(str(balance), str(amount), str(transaction_type), str(date)))
            AccountTransaction.objects.get_or_create(account=account, amount=amount, dateTime=date, type=transaction_type)


def populate():
    etfs = generateETFs()
    accounts = generateAccounts(etfs)
    #generateAccountTransaction(accounts)#generateETFHistories(etfs)
    #ats = AccountTransaction.objects.all().order_by('dateTime')
    generateProfitAccountTransaction(accounts)


if __name__ == '__main__':
    print('populating records...')
    populate()
    print('population complete!')