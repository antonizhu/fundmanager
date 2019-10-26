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
    nDays = 20
    startDate = datetime.now().date() - timedelta(days= nDays)
    price = 1.0
    riskLevel = 0;
    for etf in etfs:
        riskLevel += 1;
        for aDate in (startDate + timedelta(days= n) for n in range(nDays)):
            price += riskLevel * random.randint(-10,10)/100
            etfHistory = ETFHistory.objects.get_or_create(etf= etf, date= aDate, price= price)[0]
            etfHistory.save()

def generateAccounts(etfs):
    accounts = []
    accountsDict = [{'name': 'Francois Zhu','mobileNo': '83777384', 'selectedETF': etfs[0]},
        {'name': 'Katy Parrot','mobileNo': '83666384', 'selectedETF': etfs[1]},
        {'name': 'Kaley Coco','mobileNo': '83555384', 'selectedETF': etfs[2]},
    ]
    for accountDict in accountsDict:
        account = Account.objects.get_or_create(name=accountDict['name'], mobileNo= accountDict['mobileNo'], selectedETF = accountDict['selectedETF'])[0]
        accounts.append(account)

    for account in accounts:
        print(account)
    return accounts

def generateAccountTransaction(accounts):
    nDays = 20
    startDate = datetime.now().date() - timedelta(days= nDays)
    for account in accounts:
        for aDate in (startDate + timedelta(days= nDays) for n in range(nDays)):
            amount = round((0.1 + random.random()) % 1.0, 2)
            AccountTransaction.objects.get_or_create(account = account, amount = amount, dateTime = aDate)

def populate():
    etfs = generateETFs()
    #generateETFHistories(etfs)
    accounts = generateAccounts(etfs)
    generateAccountTransaction(accounts)

if __name__ == '__main__':
    print('populating records...')
    populate()
    print('population complete!')