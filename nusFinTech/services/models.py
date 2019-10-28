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
    etf = models.ForeignKey(ETF, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.FloatField()

    def __str__(self):
        return "{0} {1} {2}".format(self.etf, str(self.date), str(self.price))

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
    id = models.IntegerField(primary_key=True, auto_created=True, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.FloatField()
    dateTime = models.DateTimeField(auto_now_add=False)
    
    def __str__(self):
        return "{0} {1} {2} {3}".format(str(self.id), self.account, str(self.amount), str(self.dateTime))

class TransactionPrice():
    def __init__(self, accountTransaction, etfPrice, previousBalance):
        self.transactionDate = accountTransaction.dateTime.date()
        self.amount = accountTransaction.amount
        self.unitPrice = etfPrice
        self.unit = round(self.amount / self.unitPrice, 3)
        self.balance = previousBalance + self.unit

    def add(self, accountTransaction):
        addAmount = accountTransaction.amount
        addUnit = round(addAmount / self.unitPrice, 3)
        self.amount += addAmount
        self.unit += addUnit
        self.balance += addUnit

    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(self.transactionDate.strftime("%Y/%m/%d %H:%M:%S"), str(self.amount), str(self.unitPrice), str(self.unit), str(self.balance))

class AccountSummary():
    def __init__(self, account):
        transactions = AccountTransaction.objects.filter(account = account).order_by('dateTime')
        etfPrices = ETFHistory.objects.filter(etf = account.selectedETF, date__lte = datetime.today()).order_by('date')

        self.transactionLedger = []
        balance = 0

        #transaction, price and balance
        #for trxn in transactions:
        #    print("{0} {1}".format(trxn.dateTime.strftime("%Y/%m/%d %H:%M:%S"), trxn.amount))

        #for etfPrice in etfPrices:
        #    print("{0} {1}".format(etfPrice.date.strftime("%Y/%m/%d %H:%M:%S"), str(etfPrice.price)))

        for trxn in transactions:
            #print("TRX {0} {1}".format(trxn.dateTime.strftime("%Y/%m/%d %H:%M:%S"), trxn.amount))

            matchEtfDate = list(filter(lambda etf : etf.date == trxn.dateTime.date(), etfPrices))
            #for etfPrice in matchEtfDate:
            #   print("ETF {0} {1}".format(etfPrice.date.strftime("%Y/%m/%d %H:%M:%S"), str(etfPrice.price)))
            
            if(len(matchEtfDate) > 0):
                foundSameDateTrxn = False
                for transactionPrice in self.transactionLedger:
                    if (transactionPrice.transactionDate == trxn.dateTime.date()):
                        transactionPrice.add(trxn)
                        balance = transactionPrice.balance
                        foundSameDateTrxn = True
                        break
                
                if not foundSameDateTrxn:
                    transactionPrice = TransactionPrice(trxn, matchEtfDate[0].price, balance)
                    balance = transactionPrice.balance
                    self.transactionLedger.append(transactionPrice)

        for trxn in self.transactionLedger:
            print(trxn)
