from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from tenants.utils import tenant_from_request
from .models import Deal, Price
from shutters.models import Shutter, Material
from customers.models import Customer
from forms.forms import DealForm, CustomerForm, ShutterForm, PriceForm

# -----------------------------------------------
# CREATE VIEWS
# -----------------------------------------------
def add_customer(request):
    tenant = tenant_from_request(request)
    f = CustomerForm(initial={'tenant': tenant.id})

    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            # create deal for new customer
            deal = Deal.objects.create(customer_id=form.instance.id, tenant_id=tenant.id, agent=request.user, measured_by=request.user)
            price = Price.objects.create(deal_id=deal.id, tenant_id=tenant.id)
            material = Material.objects.create(deal_id=deal.id, tenant_id=tenant.id)
            return redirect(reverse('deals:add-deal-item', kwargs={'pk': deal.id}))

    return render(request, 'core/form_template.html', {'form': f, 'create': True, 'form_name': 'Customer', 'create': True})


def add_deal_item(request, pk):
    tenant = tenant_from_request(request)
    f = ShutterForm(initial={'deal': pk, 'tenant': tenant.id})
    items = Shutter.objects.filter(deal_id=pk)

    if request.method == 'POST':
        form = ShutterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('deals:add-deal-item', kwargs={'pk': pk}))

    return render(request, 'core/form_template.html', {'form': f, 'items': items, 'deal_id':pk, 'form_name': 'Item', 'create': True})


def add_deal_price(request, pk):
    shutter = Shutter.objects.filter(deal_id=pk)
    price = Price.objects.get(deal_id=pk)

    # calculate deal totals
    subtotal = round(sum(i.total_price() for i in shutter), 2)
    price.subtotal = subtotal
    price.tax = price.subtotal * price.tax_rate
    price.credit_card_fee = price.subtotal * price.credit_card_fee_rate
    price.total = subtotal + price.tax + price.credit_card_fee
    price.balance = price.total
    price.save()

    return redirect(reverse('deals:add-material', kwargs={'pk': pk}))


def add_material(request, pk):
    shutter = Shutter.objects.filter(deal_id=pk)
    material = Material.objects.get(deal_id=pk)

    material.l_frame_material = round(sum(i.l_frame_material() for i in shutter))
    material.louver_material = round(sum(i.louver_material() for i in shutter))
    material.rail_material = round(sum(i.rail_material() for i in shutter))
    material.stile_material = round(sum(i.stile_material() for i in shutter))
    material.tilt_rod_material = round(sum(i.tilt_rod_material() for i in shutter))
    material.panel_material = round(sum(i.panel_material() for i in shutter))
    material.total_hinges = round(sum(i.total_hinges() for i in shutter))
    material.total_magnets = round(sum(i.total_magnets() for i in shutter))
    material.total_screws = round(sum(i.total_screws() for i in shutter))
    material.save()

    return redirect(reverse('deals:deal-summary', kwargs={'pk': pk}))


# -----------------------------------------------
# EDIT VIEWS
# -----------------------------------------------
def edit_customer(request, pk):
    customer = Customer.objects.get(deal__id=pk)
    form = CustomerForm(request.POST or None, instance=customer)

    if form.is_valid():
        form.save()
        return redirect(reverse('deals:deal-summary', kwargs={'pk': pk}))

    return render(request, 'core/form_template.html', {'form': form, 'form_name': 'Customer', 'deal_id': pk})


def edit_deal_item(request, pk):
    shutter = Shutter.objects.get(pk=pk)
    form = ShutterForm(request.POST or None, instance=shutter)

    if form.is_valid():
        form.save()
        return redirect(reverse('deals:add-deal-price', kwargs={'pk': shutter.deal_id}))

    return render(request, 'core/form_template.html', {'form': form, 'prod_id': shutter.product_id, 'form_name': 'Item', 'deal_id': shutter.deal_id})


def edit_deal_info(request, pk):
    deal = Deal.objects.get(pk=pk)
    tenant = tenant_from_request(request)
    form = DealForm(tenant, request.POST or None, instance=deal)

    if form.is_valid():
        form.save()
        return redirect(reverse('deals:deal-summary', kwargs={'pk': pk}))

    return render(request, 'core/form_template.html', {'form': form, 'form_name': 'Deal', 'deal_id': pk})


def edit_deal_price(request, pk):
    price = Price.objects.get(pk=pk)
    form = PriceForm(request.POST or None, instance=price)

    if form.is_valid():
        f = form.save(commit=False)
        f.tax = (f.tax_rate * f.subtotal) if f.add_tax else 0
        f.add_credit_card_fee = True if f.payment_method_id == 3 else False # set to false if payment method != Credit Card
        f.credit_card_fee = (f.credit_card_fee_rate * f.subtotal) if f.add_credit_card_fee else 0
        f.total = f.subtotal + f.tax + f.credit_card_fee
        f.balance = f.total - f.down_payment
        f.save()

        return redirect(reverse('deals:deal-summary', kwargs={'pk': pk}))

    return render(request, 'core/form_template.html', {'form': form, 'price': price, 'form_name': 'Price', 'deal_id': pk})


# -----------------------------------------------
# DELETE VIEWS
# -----------------------------------------------
def confirm_delete(request, pk):
    return render(request, 'deals/confirm_action_template.html', {'pk': pk, 'action_url': 'delete-deal', 'action': 'Delete'})


def delete_deal(request, pk):
    deal = Deal.objects.get(pk=pk)
    deal.is_deleted = True
    deal.status = 'Deleted'
    deal.save()

    return redirect(reverse('core:home'))


def confirm_complete(request, pk):
    return render(request, 'deals/confirm_action_template.html', {'pk': pk, 'action_url': 'complete-deal', 'action': 'Complete'})


def complete_deal(request, pk):
    deal = Deal.objects.get(pk=pk)
    deal.is_completed = True
    deal.status = 'Completed'
    deal.save()

    return redirect(reverse('core:home'))


def confirm_restore(request, pk):
    return render(request, 'deals/confirm_action_template.html', {'pk': pk, 'action_url': 'restore-deal', 'action': 'Restore'})

def restore_deal(request, pk):
    deal = Deal.objects.get(pk=pk)
    deal.is_deleted = False
    deal.status = 'Active'
    deal.save()

    return redirect(reverse('core:home'))


class DeleteItem(DeleteView):
    model = Shutter
    template_name = 'shutters/shutter_delete.html'

    def get_success_url(self):
        return redirect(reverse('deals:add-deal-price', kwargs={'pk': self.get_object().deal_id}))
        # return reverse('deals:deal-summary', kwargs={'pk': self.get_object().deal_id})


# -----------------------------------------------
# SUMMARY VIEW
# -----------------------------------------------

def deal_summary(request, pk):
    deal = Deal.objects.get(id=pk)
    price = Price.objects.get(deal_id=pk)
    customer = Customer.objects.get(id=deal.customer_id)
    shutter = Shutter.objects.filter(deal_id=pk)

    return render(request, 'deals/deal_summary.html', {'customer': customer, 'deal': deal, 'items': shutter, 'price': price})
