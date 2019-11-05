from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import NetModel, TotalNetModel

# Create your views here.


def index(requset):
    all_netmodel = NetModel.objects.all()
    
    if requset.POST:
        post_name = requset.POST['name']
        post_value = requset.POST['value']
        post_change_type = requset.POST['change_type']
        for netmodel in all_netmodel:
            if netmodel.assets_name == post_name:
                if post_change_type == '+':
                    netmodel.total_price += int(post_value)
                else:
                    netmodel.total_price -= int(post_value)
                netmodel.save()
                break

    total_assets = 0
    new_totalnetmodel = TotalNetModel()
    for netmodel in all_netmodel:
        if netmodel.assets_type == 'Assets':
            if netmodel.currency_type != 'RMB':
                netmodel.total_price = netmodel.total_price * netmodel.exchange_rate
            total_assets = total_assets + netmodel.total_price
        else:
            total_assets = total_assets - netmodel.total_price
    new_totalnetmodel.total = total_assets
    if requset.POST:
        new_totalnetmodel.save()

    all_totalnetmodel = TotalNetModel.objects.all()
    all_totalnetmodel_date = []
    all_totalnetmodel_price = []
    for totalnetmodel in all_totalnetmodel:
        all_totalnetmodel_date.append(str(totalnetmodel.update_date))
        all_totalnetmodel_date.append(totalnetmodel.total)

    return render(requset, 'index.html', {
        'netmodel_list': all_netmodel,
        'total_assets': total_assets,
        'all_totalnetmodel_date': all_totalnetmodel_date,
        'all_totalnetmodel_price': all_totalnetmodel_price
    })


def insert(requset):
    all_netmodel = NetModel.objects.all()
    all_name = []
    for netmodel in all_netmodel:
        all_name.append(netmodel.assets_name)
    return render(requset, 'insert.html', {
        'name_list': all_name
    })
