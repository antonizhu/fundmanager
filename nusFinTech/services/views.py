from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    dict = {'insert_here': 'starting point'}
    return render(request, 'layout.html', context=dict)