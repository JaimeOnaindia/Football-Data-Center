from django.shortcuts import render

from players.models import BasePlayerStatsFBREF


def home(request):
    best_players = BasePlayerStatsFBREF.objects.all().order_by('-goals')[:5]
    return render(request, 'home.html', {'best_players': best_players})
