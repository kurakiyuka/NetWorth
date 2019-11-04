from django.shortcuts import render
from django.http import HttpResponse
from .models import NetModel

# Create your views here.

def index(requset):
    all_netmodel = NetModel.objects.all()
    if requset.POST:
        post_name = requset.POST['name']
        post_value = requset.POST['value']
        for netmodel in all_netmodel:
            if netmodel.name == post_name:
                netmodel.total_price = int(post_value)
                netmodel.save()
                break

    total_assets = 0
    for netmodel in all_netmodel:
        total_assets = total_assets + netmodel.total_price
    
    return render(requset, 'index.html', {
        'netmodel_list': all_netmodel,
        'total_assets': total_assets
    })

def insert(requset):
    all_netmodel = NetModel.objects.all()
    all_name = []
    for netmodel in all_netmodel:
        all_name.append(netmodel.name)
    return render(requset, 'insert.html', {
        'name_list': all_name
    })