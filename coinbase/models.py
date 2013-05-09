import decimal

from django.db import models
from django.conf import settings
from django.utils import timezone

import requests

from jsonfield.fields import JSONField

from .signals import order_received


class Order(models.Model):
    order_id = models.CharField(max_length=25, unique=True)
    completed_at = models.DateTimeField()
    status = models.CharField(max_length=10)
    satoshi = models.IntegerField()
    cents = models.IntegerField()
    currency_iso = models.CharField(max_length=3)
    custom = models.TextField(blank=True)
    button_type = models.CharField(max_length=100)
    button_name = models.CharField(max_length=200)
    button_description = models.TextField(blank=True)
    button_id = models.CharField(max_length=32)
    transaction_id = models.CharField(max_length=24)
    transaction_hash = models.CharField(max_length=64)
    transaction_confirmations = models.IntegerField()
    
    data = JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    
    @classmethod
    def process(cls, data):
        response = requests.get(
            "https://coinbase.com/api/v1/orders/{0}".format(
                data["order"]["id"]
            ),
            api_key=settings.COINBASE_API_KEY
        )
        verified = response.json()["order"]
        defaults = dict(
            completed_at=verified["completed_at"],
            status=verified["status"],
            satoshi=verified["total_btc"]["cents"],
            cents=verified["total_native"]["cents"],
            currency_iso=verified["total_native"]["currency_iso"],
            custom=verified["custom"],
            button_type=verified["button"]["type"],
            button_name=verified["button"]["name"],
            button_description=verified["button"]["description"],
            button_id=verified["button"]["id"],
            transaction_id=verified["transaction"]["id"],
            transaction_hash=verified["transaction"]["hash"],
            transaction_confirmations=verified["transaction"]["confirmations"],
        )
        order, created = cls.objects.get_or_create(
            order_id=verified["id"],
            defaults=defaults
        )
        if not created:
            for field in defaults:
                setattr(order, field, defaults[field])
            order.save()
        order_received.send(sender=Order, order=order)
        return order
    
    def total_bitcoin(self):
        return decimal.Decimal(str(self.satoshi / 100000000.0))
    
    def total_native(self):
        return decimal.Decimal(str(self.cents / 100.0))
