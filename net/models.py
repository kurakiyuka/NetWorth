from django.db import models

# Create your models here.

class NetModel(models.Model):
    # 资产账户名
    name = models.CharField(max_length = 100)
    # 资产账户分类
    category = models.CharField(max_length = 100)
    # 资产 / 负债
    assets_type = models.CharField(max_length = 20)
    # 币种
    currency_type = models.CharField(max_length = 10, default = 'RMB')
    # 汇率
    exchange_rate = models.IntegerField(default = 1)
    # 股票基金代号
    code = models.CharField(max_length = 10, default = '000')
    # 股票数量、基金份额
    amount = models.IntegerField(default = 0)
    # 股票基金单价
    unit_price = models.IntegerField(default = 0)
    # 股票基金总价、资产总价
    total_price = models.IntegerField(default = 0)
    # 更新时间
    update_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class TotalNetModel(models.Model):
    # 净资产
    total = models.IntegerField()
    update_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.update_date

class ModifyModel(models.Model):
    # 被更改的资产账户
    name = models.CharField(max_length = 100)
    # 更改股票数量、基金份额
    amount = models.IntegerField(default = 0)
    # 更改总价
    total_price = models.IntegerField(default = 0)
    # 增加 / 减少
    change_type = models.CharField(max_length = 20)
    # 增减的量
    change_amount = models.IntegerField(default = 0)

    def __str__(self):
        return self.name
