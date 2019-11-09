from django.db import models

# Create your models here.

ASSETS_CATEGORY_CHOICES = [('Cash', '现金'), ('Stock', '股票'), ('Fund', '基金'), ('Near Cash', '类现金'), (
        'Insurance', '保险'), ('Credit', '信用卡'), ('Bond', '债券'), ('Fixed', '定期理财'), ('Others', '其他理财'), ('Receivable', '应收'), ('payable', '应付')]
ASSETS_TYPE_CHOICES = [('Asset', '资产'), ('Debt', '负债')]

class Asset(models.Model):
    # 资产账户名
    asset_name = models.CharField(max_length=100)
    # 资产账户分类
    asset_category = models.CharField(
        max_length=100, choices=ASSETS_CATEGORY_CHOICES, default='Cash')
    # 持有账户
    holding_account = models.ForeignKey('HoldingAccount', on_delete=models.CASCADE)
    # 资产 / 负债
    asset_type = models.CharField(
        max_length=20, choices=ASSETS_TYPE_CHOICES, default='Assets')
    # 币种
    currency = models.ForeignKey('Currency', on_delete=models.DO_NOTHING, default='1')
    # 股票基金代号
    code = models.CharField(max_length=10, default='000000')
    # 股票市场
    market = models.CharField(max_length=10, null=True, blank=True)
    # 查询用的前缀
    market_prefix = models.CharField(max_length=10, null=True, blank=True)
    # 股票数量、基金份额
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # 股票基金单价
    unit_price = models.DecimalField(max_digits=14, decimal_places=4)
    # 资产总价
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    # 以人民币计价的资产总价
    total_price_in_RMB = models.DecimalField(max_digits=10, decimal_places=2)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.asset_name

class NetWorth(models.Model):
    # 净资产
    total = models.DecimalField(max_digits=10, decimal_places=2)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.update_date)

class HoldingAccount(models.Model):
    account_name = models.CharField(max_length=100)

    def __str__(self):
        return self.account_name

class Currency(models.Model):
    CURRENCY_TYPE_CHOICES = [('RMB', '人民币'), ('HKD', '港元'), ('USD', '美元')]

    currency_type = models.CharField(
        max_length=10, choices=CURRENCY_TYPE_CHOICES, default='RMB', unique=True)
    code = models.CharField(max_length=10, default='CNY')
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.currency_type

class MonthlyChange(models.Model):
    entry_name = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    changed_price = models.DecimalField(max_digits=10, decimal_places=2)
    change_account = models.ForeignKey('Asset', on_delete=models.DO_NOTHING)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.entry_name
