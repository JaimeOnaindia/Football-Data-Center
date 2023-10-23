from django.http import JsonResponse
from django.shortcuts import render
from unidecode import unidecode

from players.models import BasePlayerStatsFBREF


def home(request):
    best_players = list(BasePlayerStatsFBREF.objects.all().order_by('-goals'))
    num_players = len(best_players)
    return render(request, 'home.html',
                  {'best_players': best_players,
                   'num_players': num_players})


def search_player(request):
    query = request.GET.get('query', '')
    all_players = list(BasePlayerStatsFBREF.objects.values())
    results = [player for player in all_players
               if unidecode(query.lower()) in unidecode(player['name'].lower())]
    return JsonResponse({'results': results})
