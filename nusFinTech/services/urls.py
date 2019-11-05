from django.contrib import admin
from django.urls import path
from services import views
from services.models import ETF, ETFHistory, Account, AccountTransaction, AccountSummary
from datetime import datetime, timedelta
import random
app_name = 'services'
urlpatterns = [
    path('', views.index, name='index'),
    path('makeTransaction', views.makeTransaction, name='makeTransaction'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('timeSeriesAUM', views.timeSeriesAUM, name='timeSeriesAUM'),
    path('transactionHistory', views.transactionHistory, name='transactionHistory'),
    path('report', views.report, name='report'),
    path('monthlyReport', views.monthlyReport, name='monthlyReport'),
    path('yearlyReport', views.yearlyReport, name='yearlyReport'),
]

def updateETFHistory(nForward=0):
    print('updating etf history from last update to today...')
    etfs = ETF.objects.all()

    riskLevel = 0
    for etf in etfs:
        riskLevel += 1
        etf_history = etf.history.order_by('-date').first()
        print(etf_history)
        today_date = datetime.now().date()
        day_diff = today_date - etf_history.date
        print('{0} days to patch ETF History!'.format(day_diff.days))
        if day_diff.days > 0:
            for aDate in (etf_history.date + timedelta(days=n) for n in range(1, day_diff.days+1+nForward)):
                delta = riskLevel * random.randint(20, 40)/10000
                ETFHistory.objects.get_or_create(etf=etf, date=aDate, delta=delta)


def updateTransactionProfit(nForward=0):
    print('updating Transaction Profit history from last update to today...')
    accounts = Account.objects.all()
    for account in accounts:
        etfHistory = account.selectedETF.history.order_by('date')
        profit_txns = list(filter(lambda txn: txn.type == AccountTransaction.TYPERETURN or txn.type == AccountTransaction.TYPELOSS, account.transactions.order_by('dateTime')))
        lastProfitDate = profit_txns[-1].dateTime.date()
        today_date = datetime.today().date()

        day_diff = today_date - lastProfitDate
        print('{0} days to patch Account Profits'.format(str(day_diff.days)))
        if day_diff.days > 0:
            for aDate in (lastProfitDate + timedelta(days=n) for n in range(1, day_diff.days+1+nForward)):
                account_summary = AccountSummary(account)
                that_day_txns = list(filter(lambda txn: txn.transactionDate == aDate, account_summary.transactionLedger))
                that_day_etf_history = list(filter(lambda etfh: etfh.date == aDate, etfHistory))
                
                balance = account_summary.transactionLedger[-1].balance
                if len(that_day_txns) != 0:
                    balance = that_day_txns[0].balance
                
                delta = etfHistory.last().delta
                if len(that_day_etf_history) != 0:
                    delta = that_day_etf_history[0].delta
                
                profit = balance * delta

                type = AccountTransaction.TYPERETURN if profit > 0 else AccountTransaction.TYPELOSS
                AccountTransaction.objects.get_or_create(account=account, amount=profit, dateTime=aDate, type=type)

#updateETFHistory()

#updateTransactionProfit()