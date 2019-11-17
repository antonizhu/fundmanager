from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

import logging
logger = logging.getLogger('models')

# Create your models here.
class ETF(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{0} {1}".format(str(self.id), self.name)

class ETFHistory(models.Model):
    etf = models.ForeignKey(ETF, on_delete=models.CASCADE, related_name='history')
    date = models.DateField()
    delta = models.FloatField()
    equity_pct = models.FloatField()
    fixed_income_pct = models.FloatField()
    commodities_pct = models.FloatField()
    cash_pct = models.FloatField()

    def __str__(self):
        return "{0} {1} {2:0.3f} Eq: {3:0.3f} Fi: {4:0.3f} Co: {5:0.3f} Ca: {6:0.3f}".format(self.etf.name, str(self.date), self.delta, self.equity_pct, self.fixed_income_pct, self.commodities_pct, self.cash_pct)

class ETFMonthlySummary(models.Model):
    etf = models.ForeignKey(ETF, on_delete=models.CASCADE, related_name='monthly')
    date = models.DateField()
    delta = models.FloatField()
    equity_pct = models.FloatField()
    fixed_income_pct = models.FloatField()
    commodities_pct = models.FloatField()
    cash_pct = models.FloatField()
    def __str__(self):
        return "{0} {1} {2:0.3f} Eq: {3:0.3f} Fi: {4:0.3f} Co: {5:0.3f} Ca: {6:0.3f}".format(self.etf.name, str(self.date), self.delta, self.equity_pct, self.fixed_income_pct, self.commodities_pct, self.cash_pct)

class ETFYearlySummary(models.Model):
    etf = models.ForeignKey(ETF, on_delete=models.CASCADE, related_name='yearly')
    date = models.DateField()
    delta = models.FloatField()
    equity_pct = models.FloatField()
    fixed_income_pct = models.FloatField()
    commodities_pct = models.FloatField()
    cash_pct = models.FloatField()
    def __str__(self):
        return "{0} {1} {2:0.3f} Eq: {3:0.3f} Fi: {4:0.3f} Co: {5:0.3f} Ca: {6:0.3f}".format(self.etf.name, str(self.date), self.delta, self.equity_pct, self.fixed_income_pct, self.commodities_pct, self.cash_pct)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=250)
    mobileNo = models.CharField(max_length=10)
    selectedETF = models.ForeignKey(ETF, on_delete=models.DO_NOTHING,blank=True, null=True)
    consentGiven = models.BooleanField(default=False)

    def __str__(self):
        return "{0} {1} {2}".format(self.user.username, self.name, self.mobileNo)

class AccountTransaction(models.Model):

    TYPEDEPOSIT = 'D'
    TYPEWITHDRAW = 'W'
    TYPERETURN = 'R'
    TYPELOSS = 'L'

    TYPE_CHOICES = [(TYPEDEPOSIT, 'Deposit'), (TYPEWITHDRAW, 'Withdraw'), (TYPERETURN, 'Return'), (TYPELOSS, 'Loss')]

    id = models.IntegerField(primary_key=True, auto_created=True, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.FloatField()
    dateTime = models.DateTimeField(auto_now_add=False)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=TYPEDEPOSIT)
    
    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(str(self.id), self.account, str(self.amount), self.type, str(self.dateTime))

class MonthlySummary(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='monthly_summary')
    closing_balance = models.FloatField()
    profit = models.FloatField()
    month_year_date = models.DateTimeField()
    
    def __str__(self):
        return "{0} {1} {2} {3}".format(self.account.name, str(self.closing_balance), str(self.profit), self.month_year_date.strftime("%m/%Y"))

class YearlySummary(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='yearly_summary')
    closing_balance = models.FloatField()
    profit = models.FloatField()
    year_date = models.DateTimeField()

    def __str__(self):
        return "{0} {1} {2} {3}".format(self.account.name, str(self.closing_balance), str(self.profit), self.year_date.strftime("%Y"))

class TransactionPrice():
    def __init__(self, accountTransaction, previousBalance):
        self.transactionDate = accountTransaction.dateTime.date()
        self.amount = accountTransaction.amount
        self.profit = 0
        if (accountTransaction.type == AccountTransaction.TYPEWITHDRAW or
            accountTransaction.type == AccountTransaction.TYPELOSS):
            self.amount *= -1

        if accountTransaction.type == AccountTransaction.TYPELOSS:
            self.profit = -1.0 * accountTransaction.amount
        elif accountTransaction.type == AccountTransaction.TYPERETURN:
            self.profit = accountTransaction.amount
        

        self.balance = previousBalance + self.amount

    def add(self, accountTransaction):
        addAmount = accountTransaction.amount
        if (accountTransaction.type == AccountTransaction.TYPEWITHDRAW or
            accountTransaction.type == AccountTransaction.TYPELOSS):
            addAmount *= -1

        if accountTransaction.type == AccountTransaction.TYPELOSS:
            self.profit = -1.0 * accountTransaction.amount
        elif accountTransaction.type == AccountTransaction.TYPERETURN:
            self.profit = accountTransaction.amount

        self.balance += addAmount



    def __str__(self):
        return "{0} {1} {2} {3}".format(self.transactionDate.strftime("%Y/%m/%d %H:%M:%S"), str(self.amount), str(self.balance), str(self.profit))

class AccountSummary():
    def __init__(self, account):
        transactions = AccountTransaction.objects.filter(account=account).order_by('dateTime')
        today = datetime.now().date()
        self.last_balance = 0
        self.last_profit = 0

        self.transactionLedger = []
        balance = 0
        logger.info('total no of transactions {0}'.format(str(len(transactions))))
        for trxn in transactions:
            foundSameDateTrxn = False
            for transactionPrice in self.transactionLedger:
                if (transactionPrice.transactionDate == trxn.dateTime.date()):
                    transactionPrice.add(trxn)
                    balance = transactionPrice.balance
                    foundSameDateTrxn = True
                    break
                
            if not foundSameDateTrxn:
                transactionPrice = TransactionPrice(trxn, balance)
                balance = transactionPrice.balance
                self.transactionLedger.append(transactionPrice)

        if len(self.transactionLedger) > 0:
            
            self.last_balance = self.transactionLedger[-1].balance

            if self.transactionLedger[-1].transactionDate == today:
                if len(self.transactionLedger) > 1:
                    self.last_profit = self.transactionLedger[-2].profit
                else:
                    self.last_profit = 0
            else:
                self.last_profit = self.transactionLedger[-1].profit
