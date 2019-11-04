from django.contrib import admin
from .models import NetModel, TotalNetModel, ModifyModel

# Register your models here.

admin.site.register(NetModel)
admin.site.register(TotalNetModel)
admin.site.register(ModifyModel)