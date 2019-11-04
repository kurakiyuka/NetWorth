from django.shortcuts import render
from django.http import HttpResponse
from .models import NetModel

# Create your views here.

def hello(requset):
    all_netmodel = NetModel.objects.all()
    return render(requset, 'index.html', {
        'netmodel_list': all_netmodel
    })