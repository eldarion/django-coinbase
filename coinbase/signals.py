from django.dispatch import Signal


order_received = Signal(providing_args=["order"])
