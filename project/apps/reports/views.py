from django.shortcuts import render
from customers.models import Customer
from deals.models import Deal, Price
from shutters.models import Shutter, Material
from blinds.models import Blind
from shades.models import Shade
from sunscreens.models import Sunscreen


class Order:
    def __init__(self, **kwargs):
        self._pk = kwargs['pk']

    def deal(self):
        return Deal.objects.get(pk=self._pk)

    def customer(self):
        return Customer.objects.get(deal__id=self._pk)

    def price(self):
        return Price.objects.get(pk=self._pk)

    def shutter(self):
        return Shutter.objects.filter(deal_id=self._pk, status='Approved')

    def door_shutter(self):
        return Shutter.objects.filter(deal_id=self._pk, status='Approved').filter(shutter_type_id=4)

    def arch_shutter(self):
        return Shutter.objects.filter(deal_id=self._pk, status='Approved', shutter_type_id__in=[10, 11, 17, 18])

    def material(self):
        return Material.objects.get(pk=self._pk)

    def product_list(self):
        blind = Blind.objects.filter(deal_id=self._pk, status='Approved')
        shade = Shade.objects.filter(deal_id=self._pk, status='Approved')
        sunscreen = Sunscreen.objects.filter(deal_id=self._pk, status='Approved')

        product_list = []
        product_list.append(self.shutter()) if self.shutter() else None
        product_list.append(blind) if blind else None
        product_list.append(shade) if shade else None
        product_list.append(sunscreen) if sunscreen else None

        return product_list


def proposal_report(request, pk):
    order = Order(pk=pk)

    return render(request, 'reports/proposal_report.html', {'deal': order.deal(), 'customer': order.customer(), 'items': order.shutter(), 'product_list': order.product_list(), 'price': order.price(), 'report': 'Proposal', 'page_class': 'proposal-page'})


def invoice_report(request, pk):
    order = Order(pk=pk)

    return render(request, 'reports/invoice_report.html', {'deal': order.deal(), 'customer': order.customer(), 'items': order.shutter(), 'product_list': order.product_list(), 'price': order.price(), 'report': 'Invoice', 'page_class': 'invoice-page'})


def manufacturing_report(request, pk, product):
    order = Order(pk=pk)

    return render(request, 'reports/manufacturing_report.html', {'deal': order.deal(), 'customer': order.customer(), 'items': order.shutter(), 'product_list': order.product_list(), 'material': order.material(), 'door_shutter': order.door_shutter(), 'arch_shutter': order.arch_shutter(), 'report': 'Manufacturing Report', 'page_class': 'manufacturing-page', 'product': product})
