from django.db import models

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
    id = models.IntegerField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=250)
    mobileNo = models.CharField(max_length=10)
    selectedETF = models.ForeignKey(ETF, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{0} {1} {2}".format(str(self.id), self.name, self.mobileNo)

class AccountTransaction(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.FloatField()
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} {1} {2} {3}".format(str(self.id), self.account, str(self.amount), str(self.dateTime))