from django.db import models

# Create your models here.

ASSETS_CATEGORY_CHOICES = [('Cash', '现金'), ('Stocks', '股票'), ('Funds', '基金'), ('Near Cash', '类现金'), (
        'Insurance', '保险'), ('Credit', '信用卡'), ('Bonds', '债券'), ('Fixed', '定期理财'), ('Others', '其他理财'), ('Receivables', '应收'), ('payable', '应付')]
ASSETS_TYPE_CHOICES = [('Assets', '资产'), ('Debts', '负债')]

class NetModel(models.Model):

    # 资产账户名
    assets_name = models.CharField(max_length=100)
    # 资产账户分类
    assets_category = models.CharField(
        max_length=100, choices=ASSETS_CATEGORY_CHOICES, default='Cash')
    # 持有账户
    holding_account = models.CharField(max_length=100)
    # 资产 / 负债
    assets_type = models.CharField(
        max_length=20, choices=ASSETS_TYPE_CHOICES, default='Assets')
    # 币种
    currencytype = models.ForeignKey('CurrencyType', on_delete=models.DO_NOTHING, default='1')
    # 股票基金代号
    code = models.CharField(max_length=10, default='000000')
    # 股票市场
    market = models.CharField(max_length=10, null=True, blank=True)
    # 股票数量、基金份额
    amount = models.FloatField(default=0.0)
    # 股票基金单价
    unit_price = models.FloatField(default=0.0)
    # 股票基金总价、资产总价
    total_price = models.FloatField(default=0.0)
    # 更新时间
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.assets_name

class TotalNetModel(models.Model):
    # 净资产
    total = models.FloatField()
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.update_date)

class ModifyModel(models.Model):
    # 被更改的资产账户
    assets_name = models.CharField(max_length=100)
    # 更改股票数量、基金份额
    amount = models.FloatField(default=0.0)
    # 更改总价
    total_price = models.FloatField(default=0.0)
    # 增加 / 减少
    change_type = models.CharField(max_length=20)
    # 增减的量
    change_amount = models.FloatField(default=0.0)

    def __str__(self):
        return self.assets_name

class CurrencyType(models.Model):
    CURRENCY_TYPE_CHOICES = [('RMB', '人民币'), ('HKD', '港元'), ('USD', '美元')]

    currency_type_name = models.CharField(
        max_length=10, choices=CURRENCY_TYPE_CHOICES, default='RMB', unique=True)
    code = models.CharField(max_length=10, default='CNY')
    exchange_rate = models.FloatField(default=1.0)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.currency_type_name

class MonthlyChange(models.Model):
    entry_name = models.CharField(max_length=20)
    total_price = models.FloatField(default=0.0)
    changed_price = models.FloatField(default=0.0)
    change_account = models.ForeignKey('NetModel', on_delete=models.DO_NOTHING)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.entry_name
