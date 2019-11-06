from django.contrib import admin
from .models import NetModel, TotalNetModel, ModifyModel, CurrencyType

# Register your models here.

admin.site.register(NetModel)
admin.site.register(TotalNetModel)
admin.site.register(ModifyModel)
admin.site.register(CurrencyType)