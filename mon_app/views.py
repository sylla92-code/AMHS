import json
import random
from django.shortcuts import redirect
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
        print(data)
        id = data['id']
        temperature = data['temperature']
        tension = data['tension']
        Tableau.objects.create(id=id, temperature=temperature, tension=tension)
        return JsonResponse({'status': 'OK'})
    return JsonResponse({'error': 'PAS VALIDE'})
@csrf_exempt
def envoie(request):
    if request.method == 'POST':
        # Récupération des valeurs du formulaire
        id_value = request.POST.get('id')
        temperature = request.POST.get('temperature')
        tension = request.POST.get('tension')

        data = {
            'esp_id': int(id_value),
            'temperature': float(temperature),
            'tension': float(tension)
        }

        try:
            response = requests.post("http://10.69.211.74:8000/envoie/", json=data)
        except Exception as e:
            return JsonResponse({'status': 'ERROR', 'message': str(e)})
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # Si on arrive ici sans POST → afficher la page principale
    from .models import Tableau
    tableau = Tableau.objects.all()
    return render(request, 'index.html', {'tableau': tableau})

