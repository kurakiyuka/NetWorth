from django.shortcuts import render
from django.http import HttpResponse
from io import StringIO, BytesIO
import urllib.request
import gzip
from .models import NetModel, TotalNetModel, CurrencyType, MonthlyChange

# Create your views here.


def index(request):
    # 为Overview部分准备数据
    all_netmodel = NetModel.objects.all()
    # 生成一个holding_account组成的set()对象
    all_holding_account = set()
    for netmodel in all_netmodel:
        all_holding_account.add(netmodel.holding_account)

    # 将edit中的change存储
    if request.POST:
        post_name = request.POST['name']
        post_value = request.POST['value']
        post_change_type = request.POST['change_type']
        for netmodel in all_netmodel:
            if netmodel.assets_name == post_name:
                if post_change_type == '+':
                    netmodel.total_price += int(post_value)
                elif post_change_type == '-':
                    netmodel.total_price -= int(post_value)
                else:
                    netmodel.total_price = int(post_value)
                netmodel.save()
                break

    total_assets = 0
    new_totalnetmodel = TotalNetModel()
    for netmodel in all_netmodel:
        if netmodel.assets_type == 'Assets':
            if netmodel.currencytype.currency_type_name != 'RMB':
                netmodel.total_price = round(
                    netmodel.total_price * netmodel.currencytype.exchange_rate, 2)
            total_assets = total_assets + netmodel.total_price
        else:
            total_assets = total_assets - netmodel.total_price
    new_totalnetmodel.total = total_assets
    # 只要有POST过来，就存一份总资产
    if request.POST:
        new_totalnetmodel.save()

    # 把总资产数据都取出提供给Chart使用
    all_totalnetmodel = TotalNetModel.objects.all()
    all_totalnetmodel_date = []
    all_totalnetmodel_price = []
    for totalnetmodel in all_totalnetmodel:
        all_totalnetmodel_date.append(str(totalnetmodel.update_date)[:10])
        all_totalnetmodel_price.append(totalnetmodel.total)

    return render(request, 'index.html', {
        'netmodel_list': all_netmodel,
        'total_assets': total_assets,
        'all_holding_account': all_holding_account,
        'all_totalnetmodel_date': all_totalnetmodel_date[-10:],
        'all_totalnetmodel_price': all_totalnetmodel_price[-10:]
    })


def edit(request):
    all_netmodel = NetModel.objects.all()
    all_name = []
    for netmodel in all_netmodel:
        all_name.append(netmodel.assets_name)
    return render(request, 'edit.html', {
        'name_list': all_name
    })


def success(request):
    base_url = 'http://hq.sinajs.cn/format=text&list='
    all_netmodel = NetModel.objects.all()
    for netmodel in all_netmodel:
        if netmodel.assets_category == 'Stocks' and netmodel.market == 'usr':
            url = base_url + netmodel.market + '_' + str(netmodel.code).lower()
            response = urllib.request.urlopen(url)
            if response.getcode() == 200:
                netmodel.unit_price = float(response.read().decode('GBK').split(',')[1])
                netmodel.total_price = round(netmodel.unit_price * netmodel.amount, 2)
                netmodel.save()
            else:
                continue
        elif netmodel.assets_category == 'Stocks' and netmodel.market != 'usr':
            url = base_url + netmodel.market + netmodel.code
            response = urllib.request.urlopen(url)
            if response.getcode() == 200:
                netmodel.unit_price = float(response.read().decode('GBK').split(',')[3])
                netmodel.total_price = round(netmodel.unit_price * netmodel.amount, 2)
                netmodel.save()
            else:
                continue
        elif netmodel.assets_category == 'Funds':
            url = base_url + netmodel.market + '_' + netmodel.code
            response = urllib.request.urlopen(url)
            if response.getcode() == 200:
                netmodel.unit_price = float(response.read().decode('GBK').split(',')[1])
                netmodel.total_price = round(netmodel.unit_price * netmodel.amount, 2)
                netmodel.save()
            else:
                continue
        else:
            continue
    
    all_currency = CurrencyType.objects.all()
    for currency in all_currency:
        if currency.code != 'CNY':
            url = base_url + currency.code
            response = urllib.request.urlopen(url)
            if response.getcode() == 200:
                currency.exchange_rate = response.read().decode('GBK').split(',')[1]
                currency.save()
            else:
                continue            

    return render(request, 'success.html', {
        'all_netmodel': all_netmodel
    })

def salary(request):
    if request.POST:
        days = int(request.POST['day'])
    all_netmodel = NetModel.objects.all()
    for netmodel in all_netmodel:
        if netmodel.id == 36:
            netmodel.total_price = 19000 + round(19000 / 22 * days, 2)
            netmodel.save()
    return render(request, 'salary.html')