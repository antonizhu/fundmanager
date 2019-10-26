from django.db import models

# Create your models here.
class ETF(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ETFHistory(models.Model):
    etf = models.ForeignKey(ETF, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.FloatField()

    def __str__(self):
        return "{0} {1} {2}".format(self.etf, str(self.date), str(self.price))