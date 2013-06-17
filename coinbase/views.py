import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from .models import Order


@csrf_exempt
def handle_order_callback(request):
    if settings.COINBASE_SHARED_SECRET != request.GET.get("secret"):
        return HttpResponseForbidden()
    Order.process(json.loads(request.body))
    return HttpResponse()
