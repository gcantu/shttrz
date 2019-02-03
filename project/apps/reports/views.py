from django.shortcuts import render
from customers.models import Customer
from deals.models import Deal, Price
from shutters.models import Shutter, Material
from blinds.models import Blind
from shades.models import Shade
from sunscreens.models import Sunscreen
from django.db.models import Count
from shutters.utils import as_fraction

def proposal_report(request, pk):
    deal = Deal.objects.get(pk=pk)
    customer = Customer.objects.get(deal__id=pk)
    shutter = Shutter.objects.filter(deal_id=pk)
    blind = Blind.objects.filter(deal_id=pk)
    shade = Shade.objects.filter(deal_id=pk)
    sunscreen = Sunscreen.objects.filter(deal_id=pk)
    price = Price.objects.get(pk=pk)

    product_list = [shutter, blind, shade, sunscreen]

    return render(request, 'reports/proposal_report.html', {'deal': deal, 'customer': customer, 'price': price, 'items': shutter, 'report': 'Proposal', 'page_class': 'proposal-page', 'product_list': product_list})


def manufacturing_report(request, pk, product):
    deal = Deal.objects.get(pk=pk)
    customer = Customer.objects.get(deal__id=pk)
    shutter = Shutter.objects.filter(deal_id=pk).exclude(shutter_type_id__in=[4, 10, 11, 17, 18]).order_by('shutter_type_id')
    door_shutter = Shutter.objects.filter(deal_id=pk).filter(shutter_type_id=4)
    arch_shutter = Shutter.objects.filter(shutter_type_id__in=[10, 11, 17, 18])
    blind = Blind.objects.filter(deal_id=pk)
    shade = Shade.objects.filter(deal_id=pk)
    sunscreen = Sunscreen.objects.filter(deal_id=pk)
    material = Material.objects.get(pk=pk)

    product_list = []
    product_list.append(shutter) if shutter else None
    product_list.append(blind) if blind else None
    product_list.append(shade) if shade else None
    product_list.append(sunscreen) if sunscreen else None

    fieldname = ['louver', 'finish', 'color', 'stain', 'frame_style', 'trim_style', 'tilt_rod', 'hinge_color']

    specs = {}
    for i in range(0, len(fieldname)):
        field = fieldname[i] if i < 3 else fieldname[i] + '__' + fieldname[i]
        val = set(shutter.values_list(field, flat=True).distinct())

        if len(val) == 1:
            if field == 'louver':
                specs[fieldname[i]] = as_fraction(val.pop() or 0)
            else:
                specs[fieldname[i]] = val.pop()
        else:
            specs[fieldname[i]] = ''

    return render(request, 'reports/manufacturing_report.html', {'deal': deal, 'customer': customer, 'items': shutter, 'material': material, 'report': 'Manufacturing Report', 'specs': specs, 'page_class': 'manufacturing-page', 'product_list': product_list, 'product': product, 'door_shutter': door_shutter, 'arch_shutter': arch_shutter})


def invoice_report(request, pk):
    deal = Deal.objects.get(pk=pk)
    customer = Customer.objects.get(deal__id=pk)
    shutter = Shutter.objects.filter(deal_id=pk)
    blind = Blind.objects.filter(deal_id=pk)
    shade = Shade.objects.filter(deal_id=pk)
    sunscreen = Sunscreen.objects.filter(deal_id=pk)
    price = Price.objects.get(pk=pk)

    product_list = [shutter, blind, shade, sunscreen]

    return render(request, 'reports/invoice_report.html', {'deal': deal, 'customer': customer, 'price': price, 'items': shutter, 'report': 'Invoice', 'page_class': 'invoice-page', 'product_list': product_list})
