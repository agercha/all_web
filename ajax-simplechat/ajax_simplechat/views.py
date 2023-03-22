from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from ajax_simplechat.models import AjaxItem

import json


@login_required
@ensure_csrf_cookie
def home(request):
    # if not request.user.email.endswith("@andrew.cmu.edu"):
    #     return render(request, 'ajax_simplechat/unauthorized.html')

    return render(request, 'ajax_simplechat/index.html', {})


def get_list_json_dumps_serializer(request):
    # To make quiz11 easier, we permit reading the list without logging in. :-)
    # if not request.user.id:
    #     return _my_json_error_response("You must be logged in to do this operation", status=403)

    response_data = []
    for model_item in AjaxItem.objects.all():
        my_item = {
            'id': model_item.id,
            'text': model_item.text,
            # 'ip_addr': str(model_item.ip_addr),
            'user': model_item.user.username,
        }
        response_data.append(my_item)

    response_json = json.dumps(response_data)

    return HttpResponse(response_json, content_type='application/json')

    # To make quiz11 work, we need to allow cross-origin access
    # But normally, we would just return the HTTPResponse (like the other examples do, below)
    # response = HttpResponse(response_json, content_type='application/json')
    # response['Access-Control-Allow-Origin'] = '*'
    # return response


def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)


def add_item(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not 'item' in request.POST or not request.POST['item']:
        return _my_json_error_response("You must enter an item to add.", status=400)

    new_item = AjaxItem(text=request.POST['item'], user=request.user)
    new_item.save()

    return get_list_json_dumps_serializer(request)


def delete_item(request, item_id):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    try:
        item = AjaxItem.objects.get(id=item_id)
    except ObjectDoesNotExist:
        return _my_json_error_response(f"Item with id={item_id} does not exist.", status=404)

    if request.user.email != item.user.email:
        return _my_json_error_response("You cannot delete other user's entries", status=403)

    item.delete()

    return get_list_json_dumps_serializer(request)


def get_list_django_serializer(request):
    response_json = serializers.serialize('json', AjaxItem.objects.all())
    return HttpResponse(response_json, content_type='application/json')


def get_list_xml(request):
    response_json = serializers.serialize('xml', AjaxItem.objects.all())
    return HttpResponse(response_json, content_type='application/xml')


def get_list_xml_template(request):
    context = { 'items': AjaxItem.objects.all() }
    return render(request, 'ajax_simplechat/items.xml', context, content_type='application/xml')
