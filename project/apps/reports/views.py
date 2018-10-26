from django.shortcuts import render
from customers.models import Customer
from deals.models import Deal, Price
from shutters.models import Shutter, Material

def proposal_report(request, pk):
    deal = Deal.objects.get(pk=pk)
    customer = Customer.objects.get(deal__id=pk)
    shutter = Shutter.objects.filter(deal_id=pk)
    price = Price.objects.get(pk=pk)

    return render(request, 'reports/proposal_report.html', {'deal': deal, 'customer': customer, 'price': price, 'items': shutter, 'report': 'Proposal'})


def manufacturing_report(request, pk):
    deal = Deal.objects.get(pk=pk)
    customer = Customer.objects.get(deal__id=pk)
    shutter = Shutter.objects.filter(deal_id=pk).order_by('product_id')
    material = Material.objects.get(pk=pk)

    return render(request, 'reports/manufacturing_report.html', {'deal': deal, 'customer': customer, 'items': shutter, 'material': material, 'report': 'Manufacturing Report'})


def invoice_report(request, pk):
    deal = Deal.objects.get(pk=pk)
    customer = Customer.objects.get(deal__id=pk)
    shutter = Shutter.objects.filter(deal_id=pk)
    price = Price.objects.get(pk=pk)

    return render(request, 'reports/invoice_report.html', {'deal': deal, 'customer': customer, 'price': price, 'items': shutter, 'report': 'Invoice'})
