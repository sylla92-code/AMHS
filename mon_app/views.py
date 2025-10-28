import json

import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Tableau

# Create your views here.
def index_view(request):
    return render(request, 'index.html', context={'tableau': Tableau.objects.all()})

from django.http import JsonResponse

@csrf_exempt
def receive(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data['ID']
        temperature = data['temperature']
        tension = data['tension']
        Tableau.objects.create(ID=id, temperature=temperature, tension=tension)
        return JsonResponse({'status': 'OK'})
    return JsonResponse({'error': 'PAS VALIDE'})

def envoie(request):
    data = {
        'ID': 92,
        'temperature': 92,
        'tension': 92
    }
    return JsonResponse(data)
