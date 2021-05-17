from django.shortcuts import render, redirect
from game.models import Game
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def homeView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        option = request.POST.get('option')
        room_code = request.POST.get('room_code')

        if option == '1':
            # user have room id
            game = Game.objects.filter(room_code=room_code).first()

            if game is None:
                return HttpResponse("Room Code does not exists")

            if game.is_over:
                messages.success(request, "Game is Over")
                return redirect('/')

            game.game_opponent = username
            game.save()
            return redirect('/play/' + room_code + '?username='+username)

        else:
            game = Game(room_code=room_code, game_creator=username)
            game.save()
            return redirect('/play/' + room_code + '?username='+username)
                

    return render(request, 'game/home.html')

def gameView(request, room_code):
    username = request.GET.get('username')
    context = {
        'room_code':room_code,
        'username': username,
    }
    return render(request, 'game/game.html', context)