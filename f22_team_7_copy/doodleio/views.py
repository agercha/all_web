from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from doodleio.forms import LoginForm, GuessForm

from doodleio.models import ChatItem, PlayerItem

import json
import time
import math
import random
import os

WORD = ""
WORDS = ["jeff eppinger\n"]
START_TIME = None
ROUND = 0

def getPlayers():
    all_players_in = True
    num_guessed = 0
    all_players = []
    for player in PlayerItem.objects.all():
        all_players_in = all_players_in and player.inGameRoom
        if not player.inGameRoom: color = 'grey'
        elif player.isDrawing: color = '#FF8080'
        elif player.guessedRight:
            color = '#98CC28'
            num_guessed += 1
        else: color = '#C780FF'
        all_players.append({'name': player.name,
            'color':color, 'score': player.score,
            'guessed': str(player.guessedRight).lower()})
    all_players.sort(key=(lambda x: -x['score']))

    return (all_players_in, num_guessed, all_players)

def new_round(request):
    global START_TIME
    global ROUND
    if START_TIME != None:
        PlayerItem.get_players_drawing_status()

        #Changing current drawer
        for player in PlayerItem.objects.all():
            if player.isDrawing:
                player.hasDrawn = True
                player.isDrawing = False
                player.save()
                break

        #Choosing new drawer
        found_new = False
        for player in PlayerItem.objects.all():
            if (player.hasDrawn == False):
                found_new = True
                player.isDrawing = True
                curr_user = player
                player.save()
                break

        #picking a new word
        # with open(os.path.abspath(os.getcwd()) + "/doodleio/static/wordlist.txt", "r") as myfile:
        #     words = myfile.readlines()
        global WORD
        global WORDS
        WORD = (random.choice(WORDS))[:-1]
        WORDS.remove(WORD + "\n")
        START_TIME = None
        ROUND += 1

        #reseting all other fields
        for player in PlayerItem.objects.all():
            player.guessedRight = False
            player.word = WORD
            player.save()

        PlayerItem.get_players_drawing_status()

    return redirect(reverse('game'))

def get_chat_json_dumps_serializer(request):
    chat_data = []
    for chat in ChatItem.objects.all():
        # if chat.text == "has entered the room": color = 'grey'
        # elif chat.text == "has correctly guessed the word": color = 'LimeGreen'
        # else: color = 'black'
        weight = "normal" if chat.color == "black" else "bold"
        curr_chat = {
            'id': chat.id,
            'text': chat.text,
            'user': chat.user,
            'color': chat.color,
            'weight': weight,
        }
        chat_data.append(curr_chat)

    (all_players_in, num_guessed, all_players) = getPlayers()

    global START_TIME

    total_time = 60

    if all_players_in:
        if START_TIME == None:
            START_TIME = time.time()
            time_left = total_time
        elif num_guessed >= len(all_players) - 1:
            time_left = 0
        else:
            time_passed = time.time() - START_TIME
            time_left = max(0, math.ceil(total_time - time_passed))
    else:
        START_TIME = None
        time_left = total_time

    curr_user = PlayerItem.objects.get(name=request.user.username)

    global ROUND

    hidden_word = ""
    for i in range(len(WORD)):
        if WORD[i] == " ": hidden_word += " "
        else: hidden_word += "_"


    response_json = json.dumps({'chats': chat_data,
        'all_players_in': all_players_in,
        'all_players': all_players,
        'time_left': time_left,
        'can_draw': (str(curr_user.isDrawing)).lower(),
        'target_word': str(WORD),
        'hidden_target_word': hidden_word,
        'blank_target_word': len(WORD),
        'round': ROUND})

    return HttpResponse(response_json, content_type='application/json')

def get_users(request):
    return HttpResponse(len(PlayerItem.objects.all()), content_type='application/json')

def get_users_leaderboard(request):
    for player in PlayerItem.objects.all():
        if not player.inLeaderBoardRoom:
            return HttpResponse(False, content_type='application/json')
    return HttpResponse(True, content_type='application/json')

def login_action(request):
    context = {"display_style": ""}
    # curr_user = None

    if request.user.is_authenticated:
        curr_player = PlayerItem.objects.get(name=request.user.username)
        curr_user = User.objects.get(username=request.user.username)
        logout(request)

        curr_player.delete()
        curr_user.delete()

    for p in PlayerItem.objects.all():
        if p.inGameRoom:
            context = {"error": "cannot join while game in progress",
                "display_style": "none"}
            return render(request, 'doodleio/home.html', context)

    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'doodleio/home.html', context)

    form = LoginForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'doodleio/home.html', context)

    new_username = form['username']
    context = {'form':form, 'username':new_username}

    new_user = User.objects.create_user(username=form.cleaned_data['username'],password="")
    new_user.save()
    new_user = authenticate(username=form.cleaned_data['username'],password="")

    login(request, new_user)

    player = PlayerItem(isDrawing = False,
        hasDrawn = False,
        inGameRoom = False,
        inLeaderBoardRoom = False,
        guessedRight = False,
        word = "",
        score = 0,
        startTime = -1,
        name = request.user.username)
    player.save()
    return waiting(request, context)

@login_required
def waiting(request, context = {}):
    context["num_players"] = len(PlayerItem.objects.all())
    n = context["num_players"]
    return render(request, 'doodleio/waitingroom.html',  context)

def try_enter(request):
    if len(PlayerItem.objects.all()) >= 3:
        has_artist = False
        curr_user = None
        for player in (PlayerItem.objects.all()):
            if player.name == request.user.username: curr_user = player
            if player.isDrawing: has_artist = True

        if not has_artist:
            curr_user.isDrawing = True
            global WORD
            global WORDS
            with open(os.path.abspath(os.getcwd()) + "/doodleio/static/wordlist.txt", "r") as myfile:
                WORDS = myfile.readlines()
            WORD = (random.choice(WORDS))[:-1]
            WORDS.remove(WORD + "\n")
            warning_chat = ChatItem(text="WAIT FOR ALL USERS TO JOIN TO DRAW",
                user="",
                correct_guess=False,
                color="red")
            warning_chat.save()
            # WORD = "Jeff Eppinger"
        curr_user.inGameRoom = True
        curr_user.save()
        new_item = ChatItem(text="has entered the room",
            user=request.user.get_username(),
            correct_guess=False,
            color="grey")
        new_item.save()
        return redirect(reverse('game'))
    else:
        return render(request, 'doodleio/waitingroom.html', {})

@login_required
def game_action(request, context={}):
    curr_user = PlayerItem.objects.get(name=request.user.username)
    (_, _, players) = getPlayers()
    global START_TIME

    hidden_word = ""
    for i in range(len(WORD)):
        if WORD[i] == " ": hidden_word += " "
        else: hidden_word += "_"

    if START_TIME == None:
        time_left = 60
    else:
        time_left = max(0, math.ceil(60 - (time.time() - START_TIME)))
    context = {
        'players': players,
        'can_draw': (str(curr_user.isDrawing)).lower(),
        'target_word': str(WORD),
        'hidden_target_word': hidden_word,
        'blank_target_word': len(WORD),
        'timer_over': 'false',
        'time_left': time_left
    }
    if request.method == 'GET':
        context['form'] = GuessForm()
        return render(request, 'doodleio/game.html', context)
    return render(request, 'doodleio/game.html', context)

def _my_json_error_response(message, status=200):
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)

def add_chat(request):
    if not request.user.username:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    curr_player = PlayerItem.objects.get(name=request.user.username)

    if 'text' in request.POST and request.POST['text'] and request.user:
        is_correct = (not curr_player.isDrawing) and (WORD.lower() == request.POST['text'].lower())

        if is_correct and not curr_player.guessedRight:
            new_item = ChatItem(text="has correctly guessed the word",
                user=request.user.get_username(),
                correct_guess = False, color = "LimeGreen")
            curr_player.guessedRight = True
            time_passed = time.time() - START_TIME
            time_left = max(0, math.ceil(60 - time_passed))
            curr_player.score = curr_player.score + time_left*100
            curr_player.save()
        else:
            new_item = ChatItem(text=request.POST['text'],
                user=request.user.get_username() + ":",
                correct_guess=is_correct,
                color="black")
        new_item.save()

        return get_chat_json_dumps_serializer(request)

@login_required
def leaderboard(request):
    curr_player = PlayerItem.objects.get(name=request.user.username)
    curr_player.inLeaderBoardRoom = True
    curr_player.save()

    (_,_,player_data) = getPlayers()

    context = {'players': player_data}

    return render(request, 'doodleio/leaderboard.html', context)

def game_over(request):
    global WORD
    global START_TIME
    global ROUND
    WORD = None
    START_TIME = None
    ROUND = 0
    ChatItem.objects.all().delete()
    PlayerItem.objects.all().delete()
    User.objects.all().delete()
    if request.method == 'POST':
        return render(request, 'doodleio/gameover.html', {})
    return render(request, 'doodleio/home.html', {'form' : LoginForm()})
