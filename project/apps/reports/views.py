from django.shortcuts import render
from customers.models import Customer
from deals.models import Deal, Price
from shutters.models import Shutter, Material
from django.db.models import Count
from shutters.utils import as_fraction

def proposal_report(request, pk):
    deal = Deal.objects.get(pk=pk)
    customer = Customer.objects.get(deal__id=pk)
    shutter = Shutter.objects.filter(deal_id=pk)
    price = Price.objects.get(pk=pk)

    return render(request, 'reports/proposal_report.html', {'deal': deal, 'customer': customer, 'price': price, 'items': shutter, 'report': 'Proposal'})


def manufacturing_report(request, pk):
    deal = Deal.objects.get(pk=pk)
    customer = Customer.objects.get(deal__id=pk)
    shutter = Shutter.objects.filter(deal_id=pk).order_by('product_type_id')
    material = Material.objects.get(pk=pk)

    fieldname = ['louver', 'finish', 'color', 'stain', 'frame_style', 'trim_style', 'tilt_rod', 'hinge_color']

    specs = {}
    for i in range(0, len(fieldname)):
        field = fieldname[i] if i < 3 else fieldname[i] + '__' + fieldname[i]
        val = set(shutter.values_list(field, flat=True).distinct())

        if len(val) == 1:
            if field == 'louver':
                specs[fieldname[i]] = as_fraction(val.pop())
            else:
                specs[fieldname[i]] = val.pop()
        else:
            specs[fieldname[i]] = ''

    return render(request, 'reports/manufacturing_report.html', {'deal': deal, 'customer': customer, 'items': shutter, 'material': material, 'report': 'Manufacturing Report', 'specs': specs})


def invoice_report(request, pk):
    deal = Deal.objects.get(pk=pk)
    customer = Customer.objects.get(deal__id=pk)
    shutter = Shutter.objects.filter(deal_id=pk)
    price = Price.objects.get(pk=pk)

    return render(request, 'reports/invoice_report.html', {'deal': deal, 'customer': customer, 'price': price, 'items': shutter, 'report': 'Invoice'})
