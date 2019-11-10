from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
import urllib.request
from decimal import *
from .models import Asset, NetWorth, Currency, MonthlyChange, HoldingAccount

# Create your views here.

def index(request):
    # 为Overview部分准备数据
    all_assets = Asset.objects.all()
    # 生成一个holding_account组成的set()对象
    all_holding_accounts = set()
    for asset in all_assets:
        all_holding_accounts.add(asset.holding_account)

    # 将edit中的change存储
    if request.POST:
        post_name = request.POST['name']
        post_value = request.POST['value']
        post_change_type = request.POST['change_type']
        for asset in all_assets:
            if asset.asset_name == post_name:
                if post_change_type == '+':
                    asset.total_price += int(post_value)
                elif post_change_type == '-':
                    asset.total_price -= int(post_value)
                else:
                    asset.total_price = int(post_value)
                asset.save()
                break

    new_totalnetmodel = NetWorth()
    asset_dict = Asset.objects.values('asset_type').annotate(sum = Sum('total_price_in_RMB'))
    total_assets = round(abs(asset_dict[0]['sum'] - asset_dict[1]['sum']), 2)
    new_totalnetmodel.total = total_assets
    # 只要有POST过来，就存一份总资产
    if request.POST:
        new_totalnetmodel.save()

    # 把总资产数据都取出提供给Chart使用
    all_totalnetmodel = NetWorth.objects.all()
    all_totalnetmodel_date = []
    all_totalnetmodel_price = []
    for totalnetmodel in all_totalnetmodel:
        all_totalnetmodel_date.append(str(totalnetmodel.update_time)[:10])
        all_totalnetmodel_price.append(float(totalnetmodel.total))

    return render(request, 'index.html', {
        'all_assets': all_assets,
        'total_assets': total_assets,
        'all_holding_account': all_holding_accounts,
        'all_totalnetmodel_date': all_totalnetmodel_date[-10:],
        'all_totalnetmodel_price': all_totalnetmodel_price[-10:]
    })


def edit(request):
    all_assets_name = Asset.objects.values_list('asset_name', flat=True)
    return render(request, 'edit.html', {
        'all_assets_name': all_assets_name
    })


def success(request):
    base_url = 'http://hq.sinajs.cn/format=text&list='

    all_currencies = Currency.objects.all().exclude(code='CNY')
    for currency in all_currencies:
        url = base_url + currency.code
        response = urllib.request.urlopen(url)
        if response.getcode() == 200:
            currency.exchange_rate = response.read().decode(
                'GBK').split(',')[1]
            currency.save()
        else:
            continue

    all_assets = Asset.objects.all().exclude(code='000000')
    for asset in all_assets:
        url = base_url + asset.market_prefix + str(asset.code).lower()
        response = urllib.request.urlopen(url)
        if response.getcode() == 200:
            if asset.asset_category == 'Stock' and asset.market != 'usr':
                asset.unit_price = Decimal(
                    response.read().decode('GBK').split(',')[3])
            else:
                asset.unit_price = Decimal(
                    response.read().decode('GBK').split(',')[1])

            asset.total_price = asset.unit_price * asset.amount
            asset.total_price_in_RMB = asset.total_price * asset.currency.exchange_rate
            asset.save()

        else:
            continue

    return render(request, 'success.html', {
        'all_assets': all_assets
    })


def salary(request):
    if request.POST:
        days = int(request.POST['day'])
    Asset.objects.filter(id=36).update(
        total_price=19000 / 22 * days, total_price_in_RMB=19000 / 22 * days)
    return render(request, 'salary.html')
