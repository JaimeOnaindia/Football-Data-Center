from django.http import JsonResponse
from django.shortcuts import render
from unidecode import unidecode

from players.models import BasePlayerStatsFBREF


def home(request):
    all_players = BasePlayerStatsFBREF.objects.all().order_by('-goals')
    num_players = all_players.count()
    return render(request, 'tables-data.html',
                  {'best_players': list(all_players)[:100],
                   'num_players': num_players})


def search_player(request):
    query = request.GET.get('query', '')
    all_players = list(BasePlayerStatsFBREF.objects.values())
    results = [player for player in all_players
               if unidecode(query.lower()) in unidecode(player['name'].lower())]
    return JsonResponse({'results': results})
