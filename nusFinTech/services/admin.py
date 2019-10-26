from django.contrib import admin
from services.models import ETF, ETFHistory

# Register your models here.
admin.site.register(ETF)
admin.site.register(ETFHistory)