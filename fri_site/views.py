from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import User, Message
from .forms import MessageForm
from datetime import datetime
import telebot
import json
import os


def index(request):
    to_do = Message.objects.filter(status__exact='to do').order_by('-date')
    in_progress = Message.objects.filter(status__exact='in progress').order_by('-date')
    done = Message.objects.filter(status__exact='done').order_by('-date')
    context = {"to_do": to_do, "in_progress": in_progress, "done": done}
    return render(request, 'fri_site/index.html', context)


@csrf_exempt
def add_user_and_message_from_bot(request):

    tg_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", None)
    assert tg_bot_token is not None, "TELEGRAM_BOT_TOKEN should be set as env variable"

    bot = telebot.TeleBot(tg_bot_token)

    try:
        json_message = json.loads(request.body)
    except json.decoder.JSONDecodeError as err:
        return HttpResponse(str(err))

    def _user_exists(user_id: int) -> bool:
        if User.objects.filter(user_id__exact=user_id).count() > 0:
            return True
        return False

    def _update_id_exists(update_id: int) -> bool:
        if Message.objects.filter(update_id__exact=update_id).count() > 0:
            return True
        return False

    def _add_user_to_db(json_dict: dict) -> (None, True):
        try:
            user_id = json_dict['message']['from'].get('id')
            first_name = json_dict['message']['from'].get('first_name')
            last_name = json_dict['message']['from'].get('last_name')
            username = json_dict['message']['from'].get('username')
        except KeyError:
            return None

        if None in (user_id, first_name):
            return None

        if _user_exists(user_id):
            return True

        try:
            User(
                user_id=int(user_id),
                first_name=str(first_name),
                last_name=last_name,
                user_name=username,
            ).save()
            return True
        except (KeyError, ValueError):
            return None

    def _add_message_to_db(json_dict: dict) -> (None, True):
        try:
            sender_id = json_dict['message']['from'].get('id')
            sender_object = User.objects.filter(user_id__exact=sender_id).get()
            message_text = json_dict['message'].get('text')
            message_date = json_dict['message'].get('date')
            update_id = json_dict.get('update_id')
        except KeyError:
            return None

        if None in (sender_id, update_id, message_text, message_date):
            return None

        if _update_id_exists(update_id):
            return True

        try:
            Message(
                update_id=int(update_id),
                message=str(message_text),
                sender=sender_object,
                date=datetime.fromtimestamp(int(message_date)),
            ).save()
            return True
        except (KeyError, ValueError):
            return None

    try:
        result_user = _add_user_to_db(json_message)
        result_mes = _add_message_to_db(json_message)
    except ValueError as e:
        return HttpResponseBadRequest(str(e))
    if result_user is True and result_mes is True:
        response = "Привіт!\nМи отримали твій запит, подумаємо над ним і відпишемо, як тільки зможемо :)"
        bot.send_message(json_message['message']['chat'].get('id'), response)
        return HttpResponse('OK')
    else:
        return HttpResponseBadRequest('Malformed or incomplete JSON data received')


def edit_message(request, update_id):
    message = Message.objects.get(update_id=update_id)
    if request.method != 'POST':
        form = MessageForm(instance=message)
    else:
        form = MessageForm(instance=message, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('fri_site:index')

    context = {'message': message, 'form': form}
    return render(request, 'fri_site/edit_message.html', context)
