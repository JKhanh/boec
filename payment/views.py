# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import *

from django.conf import settings
from django.shortcuts import render, get_object_or_404, reverse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from paypal.standard.forms import PayPalPaymentsForm

from orders.models import Order


# @csrf_exempt
def payment_done(request, id):
    order = get_object_or_404(Order, id=id)
    order.paid = True
    order.save()
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')


def payment_process(request, id):
    order = get_object_or_404(Order, id=id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.get_total_cost().quantize(Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment:done', args=[order.id])),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'order': order, 'form': form})
