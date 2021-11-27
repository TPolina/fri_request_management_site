from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Request
from datetime import datetime
import json


def index(request):
    requests = Request.objects.all()
    res = "Requests: \n"
    for r in requests:
        res += f"{r.request} from {r.sender}\n"
    return HttpResponse(res)


@csrf_exempt
def show_request_on_page(request):
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
        return HttpResponse('OK')
    else:
        return HttpResponseBadRequest('Malformed or incomplete JSON data received')
