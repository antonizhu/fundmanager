from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

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

    def __str__(self):
        return "{0} {1} {2}".format(self.etf, str(self.date), str(self.delta))

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
    TYPEPROFIT = 'P'
    TYPELOSS = 'L'

    TYPE_CHOICES = [(TYPEDEPOSIT, 'Deposit'), (TYPEWITHDRAW, 'Withdraw'), (TYPEPROFIT, 'Profit'), (TYPELOSS, 'Loss')]

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
        elif accountTransaction.type == AccountTransaction.TYPEPROFIT:
            self.profit = accountTransaction.amount
        

        self.balance = previousBalance + self.amount

    def add(self, accountTransaction):
        addAmount = accountTransaction.amount
        if (accountTransaction.type == AccountTransaction.TYPEWITHDRAW or
            accountTransaction.type == AccountTransaction.TYPELOSS):
            addAmount *= -1

        if accountTransaction.type == AccountTransaction.TYPELOSS:
            self.profit = -1.0 * accountTransaction.amount
        elif accountTransaction.type == AccountTransaction.TYPEPROFIT:
            self.profit = accountTransaction.amount

        self.balance += addAmount



    def __str__(self):
        return "{0} {1} {2} {3}".format(self.transactionDate.strftime("%Y/%m/%d %H:%M:%S"), str(self.amount), str(self.balance), str(self.profit))

class AccountSummary():
    def __init__(self, account):
        transactions = AccountTransaction.objects.filter(account=account).order_by('dateTime')
        
        self.transactionLedger = []
        balance = 0
        print('total no of transactions {0}'.format(str(len(transactions))))
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

        for trxn in self.transactionLedger:
            print(trxn)
