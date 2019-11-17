import logging

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nusFinTech.settings')


import django
django.setup()


import random
from services.models import ETF, ETFHistory, Account, AccountTransaction, MonthlySummary, YearlySummary
from services.models import ETFMonthlySummary, ETFYearlySummary
from faker import Faker
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.db.models import Func, F, Avg, Count, Sum
from django.db.models.functions import TruncMonth, TruncYear

import calendar
from dateutil.relativedelta import relativedelta
import csv

fakegen = Faker()
nDays = 365

import logging
logger = logging.getLogger('populate_db')

def generateETFs():
    logger.info('TEST')
    etfList = []
    etfs = ['Low_Risk', 'Medium_Risk', 'High_Risk']
    for etf in etfs:
        logger.info('getting or creating {0}'.format(etf))
        etfObj = ETF.objects.get_or_create(name=etf)[0]
        
        etfList.append(etfObj)

    for etfObj in etfList:
        logger.info(etfObj)
        
    return etfList

def generateETFHistories(etfs):

    startDate = datetime.now().date() - timedelta(days= nDays)
    aum = [ {'eq': 0.2, 'fi': 0.2, 'co': 0.2, 'ca': 0.4}, 
            {'eq': 0.3, 'fi': 0.2, 'co': 0.3, 'ca': 0.2}, 
            {'eq': 0.4, 'fi': 0.1, 'co': 0.4, 'ca': 0.1}]
    riskLevel = 0
    for etf in etfs:
        
        for aDate in (startDate + timedelta(days= n) for n in range(nDays)):
            delta = (riskLevel + 1) * random.randint(20,40)/10000
            eq_pct = aum[riskLevel]['eq'] + random.randint(-40, 40)/10000
            fi_pct = aum[riskLevel]['fi'] + random.randint(-40, 40)/10000
            co_pct = aum[riskLevel]['co'] + random.randint(-40, 40)/10000
            ca_pct = 1 - (eq_pct + fi_pct + co_pct)
            ETFHistory.objects.get_or_create(etf=etf, date=aDate, delta=delta, equity_pct=eq_pct, 
                                                fixed_income_pct=fi_pct, commodities_pct=co_pct, cash_pct=ca_pct)
            
        riskLevel += 1

def generateETFHistoriesFromFile(etf, csv_reader):
    
    startDate = datetime.now().date() - timedelta(days=nDays)
    index = 0
    for row in csv_reader:
        logger.info('eq: {0:0.3f}, fi: {1:0.3f}, co: {2:0.3f}, ca: {3:0.3f}, d/w: {4:0.3f}, re: {5:0.3f}, total: {6:0.3f}'.format(float(row['Asset Composition - Equities']), float(row['Asset Composition - Fixed Income']), float(row['Asset Composition - Commodities']), float(row['Asset Composition - Cash']), float(row['Daily Contribution/Withdrawals']), float(row['Return Value']), float(row['Total Value'])))
        date = startDate + timedelta(days=index)
        ETFHistory.objects.get_or_create(etf=etf, date=date, delta=row['delta'], equity_pct=float(row['Asset Composition - Equities']), 
                                        fixed_income_pct=float(row['Asset Composition - Fixed Income']), 
                                        commodities_pct=float(row['Asset Composition - Commodities']), 
                                        cash_pct=float(row['Asset Composition - Cash']))
        index += 1

def generateETFMonthlySummary(etfs):
    for etf in etfs:
        monthlySummary = etf.history.annotate(month=TruncMonth('date')).values('month').annotate(delta=Sum('delta'), eq_pct=Avg('equity_pct'), fi_pct=Avg('fixed_income_pct'), co_pct=Avg('commodities_pct'), ca_pct=Avg('cash_pct')).order_by('month')
        for monthly in monthlySummary: 
            logger.info(monthly)
            end_month_day = calendar.monthrange(monthly['month'].year, monthly['month'].month)[1]
            month_year_date = monthly['month'].replace(day=end_month_day)
            ETFMonthlySummary.objects.get_or_create(etf=etf, date=month_year_date, delta=monthly['delta'], equity_pct=monthly['eq_pct'], 
                                                fixed_income_pct=monthly['fi_pct'], commodities_pct=monthly['co_pct'], cash_pct=monthly['ca_pct'])

def generateETFYearlySummary(etfs):
    for etf in etfs:
        yearlySummary = etf.history.annotate(year=TruncYear('date')).values('year').annotate(delta=Sum('delta'), eq_pct=Avg('equity_pct'), fi_pct=Avg('fixed_income_pct'), co_pct=Avg('commodities_pct'), ca_pct=Avg('cash_pct')).order_by('year')
        for yearly in yearlySummary: 
            logger.info(yearly)
            year_date = yearly['year'].replace(day=31, month=12)    
            ETFYearlySummary.objects.get_or_create(etf=etf, date=year_date, delta=yearly['delta'], equity_pct=yearly['eq_pct'], 
                                                fixed_income_pct=yearly['fi_pct'], commodities_pct=yearly['co_pct'], cash_pct=yearly['ca_pct'])


def generateAccounts(etfs):
    accounts = []
    accountsDict = [{'name': 'Jing Xia','mobileNo': '83999123', 'selectedETF': etfs[1]},
        #{'name': 'Katy Parrot','mobileNo': '83666384', 'selectedETF': etfs[1]},
        #{'name': 'Kaley Coco','mobileNo': '83555384', 'selectedETF': etfs[2]},
    ]
    for accountDict in accountsDict:
        account = Account.objects.get_or_create(name=accountDict['name'], mobileNo= accountDict['mobileNo'], selectedETF = accountDict['selectedETF'])[0]
        accounts.append(account)

    for account in accounts:
        logger.info(account)
    return accounts

def generateAccountTransaction(accounts):

    startDate = datetime.now() - timedelta(days= nDays)
    for account in accounts:
        for aDate in (startDate + timedelta(days= n) for n in range(nDays)):
            aDate = aDate.replace(hour= random.randint(9,15))

            amount = round((0.1 + random.random()) % 1.0, 2)
            AccountTransaction.objects.get_or_create(account=account, amount=amount, dateTime=aDate)

def generateAccountTransactionFromFile(account, csv_reader):
    startDate = datetime.now(tz=timezone.utc) - timedelta(days=nDays)
    index = 0
    for row in csv_reader:
        logger.info('d/w: {0:0.3f}'.format(float(row['Daily Contribution/Withdrawals'])))
        date = startDate + timedelta(days=index)
        amount = float(row['Daily Contribution/Withdrawals'])
        if amount < 0:
            type = AccountTransaction.TYPEWITHDRAW
            amount = abs(amount)
        else:
            type = AccountTransaction.TYPEDEPOSIT

        AccountTransaction.objects.get_or_create(account=account, amount=amount, dateTime=date, type=type)
        index += 1

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
            transaction_type = AccountTransaction.TYPERETURN
            if amount < 0 : 
                transaction_type = AccountTransaction.TYPELOSS
                amount = abs(amount)
            date = txn.dateTime
            date = date.replace(hour=23, minute=59, second=59)
            logger.info('{0} {1} {2} {3}'.format(str(balance), str(amount), str(transaction_type), str(date)))
            AccountTransaction.objects.get_or_create(account=account, amount=amount, dateTime=date, type=transaction_type)



nMonths = 24
def generateMonthlySummary(accounts):
    #account 1 low, account 2 medium, account 3 high
    
    risk_level = 0
    for account in accounts:

        monthlySummary = account.transactions.annotate(month=TruncMonth('dateTime')).values('month', 'type').annotate(total=Sum('amount')).order_by('month')
        
        previous_closing_balance = 0
        accountMonthlySummary = {}

        for monthly in monthlySummary:
            logger.info(monthly)
            if str(monthly['month']) not in accountMonthlySummary:
                end_month_day = calendar.monthrange(monthly['month'].year, monthly['month'].month)[1]
                month_year_date = monthly['month'].replace(day=end_month_day)
                summary = MonthlySummary(account=account, month_year_date= month_year_date, closing_balance=previous_closing_balance, profit=0)
            else:
                summary = accountMonthlySummary[str(monthly['month'])]
            
            if monthly['type'] == AccountTransaction.TYPEDEPOSIT:
                summary.closing_balance += monthly['total']
                previous_closing_balance += monthly['total']
            elif monthly['type'] == AccountTransaction.TYPEWITHDRAW:
                summary.closing_balance -= monthly['total']
                previous_closing_balance -= monthly['total']
            elif monthly['type'] == AccountTransaction.TYPERETURN:
                summary.closing_balance += monthly['total']
                previous_closing_balance += monthly['total']
                summary.profit += monthly['total']
            elif monthly['type'] == AccountTransaction.TYPELOSS:
                summary.closing_balance -= monthly['total']
                previous_closing_balance -= monthly['total']
                summary.profit -= monthly['total']
            else:
                raise Exception('unknonw transaction type: {0}'.format(str(monthly['type'])))
            
            accountMonthlySummary[str(monthly['month'])] = summary

        for monthly in accountMonthlySummary.values():
            logger.info(monthly)
            MonthlySummary.objects.get_or_create(account=monthly.account, closing_balance=monthly.closing_balance, profit=monthly.profit, month_year_date=monthly.month_year_date)
            
        
def generateYearlySummary(accounts):
    for account in accounts:
        monthly_summaries = account.monthly_summary.order_by('month_year_date')
        
        year = monthly_summaries[0].month_year_date.year
        
        profit = 0
        closing_balance = 0

        for monthly_summary in monthly_summaries:
            if year == monthly_summary.month_year_date.year:
                profit += monthly_summary.profit
                closing_balance = monthly_summary.closing_balance
                month_year_date = monthly_summary.month_year_date
            else:
                YearlySummary.objects.get_or_create(account=account, closing_balance=closing_balance, profit=profit, year_date=month_year_date)
                year = monthly_summary.month_year_date.year
                profit = monthly_summary.profit
                closing_balance = monthly_summary.closing_balance
                month_year_date = monthly_summary.month_year_date
                
        YearlySummary.objects.get_or_create(account=account, closing_balance=closing_balance, profit=profit, year_date=month_year_date)

def clearETFHistories():
     ETFHistory.objects.all().delete() 
     ETFMonthlySummary.objects.all().delete()
     ETFYearlySummary.objects.all().delete()

def clearAccountTransactions():
    AccountTransaction.objects.all().delete()
    MonthlySummary.objects.all().delete()
    YearlySummary.objects.all().delete()           

def populate():
    etfs = generateETFs()
    accounts = generateAccounts(etfs)
    
    with open('../data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        generateETFHistoriesFromFile(etfs[1], csv_reader)
    
    generateETFMonthlySummary(etfs)
    generateETFYearlySummary(etfs)

    with open('../data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        generateAccountTransactionFromFile(accounts[0], csv_reader)

    generateProfitAccountTransaction(accounts)
    generateMonthlySummary(accounts)
    generateYearlySummary(accounts)


if __name__ == '__main__':
    logger.info('populating records...')
    populate()
    logger.info('population complete!')