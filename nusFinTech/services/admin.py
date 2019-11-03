from django.contrib import admin
from services.models import ETF, ETFHistory, Account, AccountTransaction, MonthlySummary

# Register your models here.
admin.site.register(ETF)
admin.site.register(ETFHistory)
admin.site.register(Account)
admin.site.register(AccountTransaction)
admin.site.register(MonthlySummary)