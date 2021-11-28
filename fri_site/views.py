from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Request
from datetime import datetime
import telebot
import json
import os


def index(request):
    requests = Request.objects.order_by('-date')
    return render(request, 'fri_site/index.html', {'requests': requests})


@csrf_exempt
def add_request_from_bot(request):

    tg_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    assert tg_bot_token is not None, "TELEGRAM_BOT_TOKEN should be set as env variable"

    bot = telebot.TeleBot(tg_bot_token)

    try:
        json_message = json.loads(request.body)
    except json.decoder.JSONDecodeError as err:
        return HttpResponse(str(err))

    def _update_id_exists(update_id: int) -> bool:
        if Request.objects.filter(update_id__exact=update_id).count() > 0:
            return True
        return False

    def _add_message_to_db(json_dict: dict) -> (None, True):
        try:
            sender_id = json_dict['message']['from'].get('id')
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
            Request(
                update_id=update_id,
                request=str(message_text),
                sender=sender_id,
                date=datetime.fromtimestamp(int(message_date)),
                in_progress=False,
                done=False
            ).save()
            return True
        except (KeyError, ValueError):
            return None

    try:
        result = _add_message_to_db(json_message)
    except ValueError as e:
        return HttpResponseBadRequest(str(e))
    if result is True:
        response = "Привіт!\nМи отримали твій запит, подумаємо над ним і відпишемо, як тільки зможемо :)"
        bot.send_message(json_message['message']['chat'].get('id'), response)
        return HttpResponse('OK')
    else:
        return HttpResponseBadRequest('Malformed or incomplete JSON data received')
