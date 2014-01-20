import decimal

from django.test import TestCase
from django.utils import timezone

from mock import patch

from .models import Order


class OrderTests(TestCase):
    
    def setUp(self):
        self.order = Order(
            order_id="XXXXXX",
            completed_at=timezone.now(),
            status="completed",
            satoshi=23324233,
            cents=4343,
            currency_iso="USD",
            custom="",
            button_type="foo",
            button_name="foo",
            button_description="foo",
            button_id="foo",
            transaction_id="foo",
            transaction_hash="foo",
            transaction_confirmations="foo"
        )
        # pylint: disable=C0301
        self.notification_data = {
            "order": {
                "id": "5RTQNACF",
                "created_at": "2012-12-09T21:23:41-08:00",
                "status": "completed",
                "total_btc": {
                    "cents": 100000000,
                    "currency_iso": "BTC"
                },
                "total_native": {
                    "cents": 1253,
                    "currency_iso": "USD"
                },
                "custom": "order1234",
                "button": {
                    "type": "buy_now",
                    "name": "Alpaca Socks",
                    "description": "The ultimate in lightweight footwear",
                    "id": "5d37a3b61914d6d0ad15b5135d80c19f"
                },
                "transaction": {
                    "id": "514f18b7a5ea3d630a00000f",
                    "hash": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
                    "confirmations": 0
                }
            }
        }
    
    def test_satoshi_conversion(self):
        self.assertEquals(
            decimal.Decimal("0.23324233"),
            self.order.total_bitcoin()
        )
    
    def test_cents_conversion(self):
        self.assertEquals(
            decimal.Decimal("43.43"),
            self.order.total_native()
        )
    
    @patch("requests.get")
    def test_process_handling_normal_order_data(self, GetMock):
        GetMock.return_value.json.return_value = self.notification_data
        order = Order.process(self.notification_data)
        self.assertEquals(order.order_id, self.notification_data["order"]["id"])
        self.assertEquals(order.satoshi, 100000000)
        self.assertEquals(order.cents, 1253)

    @patch("requests.get")
    def test_process_handling_order_data_without_description(self, GetMock):
        self.notification_data["order"]["button"]["description"] = None
        GetMock.return_value.json.return_value = self.notification_data

        order = Order.process(self.notification_data)
        self.assertEquals(order.order_id, self.notification_data["order"]["id"])
        self.assertIsNone(order.button_description)
