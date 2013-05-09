import decimal

from django.test import TestCase
from django.utils import timezone

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
    
    def test_process_handling_normal_order_data(self):
        self.fail()
    
    def test_signal_sent(self):
        self.fail()
