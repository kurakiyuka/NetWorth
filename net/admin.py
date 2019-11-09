from django.contrib import admin
from .models import NetWorth, Currency, MonthlyChange, HoldingAccount, Asset

# Register your models here.

admin.site.register(Asset)
admin.site.register(NetWorth)
admin.site.register(HoldingAccount)
admin.site.register(Currency)
admin.site.register(MonthlyChange)