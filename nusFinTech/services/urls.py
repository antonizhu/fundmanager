from django.contrib import admin
from django.urls import path
from services import views
from services.models import ETF, ETFHistory, Account, AccountTransaction, AccountSummary
from datetime import datetime, timedelta
import random

import logging
logger = logging.getLogger('urls')

app_name = 'services'
urlpatterns = [
    path('', views.index, name='index'),
	path('portfolio_composition', views.portfolioComposition, name='portfolio_composition'),
	path('account_setting', views.accountSetting, name='account_setting'),
    path('submit_score', views.submit_score, name='submit_score'),
    path('makeTransaction', views.makeTransaction, name='makeTransaction'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('timeSeriesAUM', views.timeSeriesAUM, name='timeSeriesAUM'),
    path('transactionHistory', views.transactionHistory, name='transactionHistory'),
    path('report', views.report, name='report'),
    path('monthlyReport', views.monthlyReport, name='monthlyReport'),
    path('yearlyReport', views.yearlyReport, name='yearlyReport'),
]

def updateETFHistory(nForward=0):
    logger.info('updating etf history from last update to today...')
    etfs = ETF.objects.all()
    aum = [ {'eq': 0.2, 'fi': 0.2, 'co': 0.2, 'ca': 0.4}, 
            {'eq': 0.3, 'fi': 0.2, 'co': 0.3, 'ca': 0.2}, 
            {'eq': 0.4, 'fi': 0.1, 'co': 0.4, 'ca': 0.1}]
    riskLevel = 0

    for etf in etfs:
        etf_history = etf.history.order_by('-date').first()
        if etf_history is None:
            continue
        logger.info(etf_history)
        today_date = datetime.now().date()
        day_diff = today_date - etf_history.date
        logger.info('{0} days since last patch to ETF History!'.format(day_diff.days))
        if day_diff.days > 1:
            for aDate in (etf_history.date + timedelta(days=n) for n in range(1, day_diff.days+nForward)):
                delta = (riskLevel + 1) * random.randint(20, 40)/10000
                eq_pct = etf_history.equity_pct + random.randint(-40, 40)/10000
                fi_pct = etf_history.fixed_income_pct + random.randint(-40, 40)/10000
                co_pct = etf_history.commodities_pct + random.randint(-40, 40)/10000
                ca_pct = 1 - (eq_pct + fi_pct + co_pct)
                ETFHistory.objects.get_or_create(etf=etf, date=aDate, delta=delta, equity_pct = eq_pct, 
                                                fixed_income_pct = fi_pct, commodities_pct = co_pct, cash_pct = ca_pct)
        riskLevel += 1
        


def updateTransactionProfit(nForward=0):
    logger.info('updating Transaction Profit history from last update to yesterday...')
    accounts = Account.objects.all()
    for account in accounts:
        etfHistory = account.selectedETF.history.order_by('date')
        profit_txns = list(filter(lambda txn: txn.type == AccountTransaction.TYPERETURN or txn.type == AccountTransaction.TYPELOSS, account.transactions.order_by('dateTime')))
        if len(profit_txns) <= 0:
            continue
        
        lastProfitDate = profit_txns[-1].dateTime.date()
        today_date = datetime.today().date()

        day_diff = today_date - lastProfitDate
        logger.info('{0} days since last patch to Account Profits'.format(str(day_diff.days)))
        if day_diff.days > 1:
            for aDate in (lastProfitDate + timedelta(days=n) for n in range(1, day_diff.days+nForward)):
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

updateETFHistory()

updateTransactionProfit()