from django.urls import reverse
from django.shortcuts import render
from django.views.generic.edit import DeleteView, UpdateView
from deals.views import CustomCreateView
from customers.models import Customer
from deals.models import Deal, Price
from shutters.models import Shutter
from blinds.models import Blind
from shades.models import Shade
from sunscreens.models import Sunscreen
from forms.forms import BlindForm, ShadeForm, SunscreenForm


def select_product(request, deal_id):
    return render(request, 'premiumplans/select_product.html', {'deal_id': deal_id})

# -----------------------------------------------
# CREATE VIEWS
# -----------------------------------------------
class CreateBlindItem(CustomCreateView):
    form_class = BlindForm
    model = Blind

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blind_items'] = Blind.objects.filter(deal_id=self.kwargs.get('deal_id'))
        return context

    def get_success_url(self):
        return reverse('premiumplans:create-blind-item', kwargs={'deal_id': self.object.deal_id})


class CreateShadeItem(CustomCreateView):
    form_class = ShadeForm
    model = Shade

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shade_items'] = Shade.objects.filter(deal_id=self.kwargs.get('deal_id'))
        return context

    def get_success_url(self):
        return reverse('premiumplans:create-shade-item', kwargs={'deal_id': self.object.deal_id})


class CreateSunscreenItem(CustomCreateView):
    form_class = SunscreenForm
    model = Sunscreen

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sunscreen_items'] = Sunscreen.objects.filter(deal_id=self.kwargs.get('deal_id'))
        return context

    def get_success_url(self):
        return reverse('premiumplans:create-sunscreen-item', kwargs={'deal_id': self.object.deal_id})

# -----------------------------------------------
# EDIT VIEWS
# -----------------------------------------------
class CustomUpdateView(UpdateView):
    def get_success_url(self):
        return reverse('deals:deal-specs', kwargs={'deal_id': self.kwargs.get('deal_id')})

class UpdateBlindItem(CustomUpdateView):
    model = Blind
    form_class = BlindForm

class UpdateShadeItem(CustomUpdateView):
    model = Shade
    form_class = ShadeForm

class UpdateSunscreenItem(CustomUpdateView):
    model = Sunscreen
    form_class = SunscreenForm


# -----------------------------------------------
# DELETE VIEWS
# -----------------------------------------------
class CustomDeleteItem(DeleteView):
    def get_success_url(self):
        return reverse('deals:deal-specs', kwargs={'deal_id': self.get_object().deal_id})

class DeleteBlindItem(CustomDeleteItem):
    model = Blind

class DeleteShadeItem(CustomDeleteItem):
    model = Shade

class DeleteSunscreenItem(CustomDeleteItem):
    model = Sunscreen


# -----------------------------------------------
# SUMMARY VIEW
# -----------------------------------------------
def deal_summary(request, pk):
    deal = Deal.objects.get(id=pk)
    price = Price.objects.get(deal_id=pk)
    customer = Customer.objects.get(id=deal.customer_id)
    shutter = Shutter.objects.filter(deal_id=pk)
    blind = Blind.objects.filter(deal_id=pk)
    shade = Shade.objects.filter(deal_id=pk)
    sunscreen = Sunscreen.objects.filter(deal_id=pk)

    return render(request, 'premiumplans/deal_summary.html', {'customer': customer, 'deal': deal, 'items': shutter, 'price': price, 'blind_items': blind, 'shade_items': shade, 'sunscreen_items': sunscreen})
