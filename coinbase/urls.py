from django.conf.urls import patterns, url


urlpatterns = patterns(
    "coinbase.views",
    url(r"^cb/$", "handle_order_callback", name="coinbase_order_callback")
)
