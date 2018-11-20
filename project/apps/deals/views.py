from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic import ListView
from tenants.utils import tenant_from_request
from .models import Deal, Price
from shutters.models import Shutter, Material
from customers.models import Customer
from forms.forms import DealForm, CustomerForm, ShutterForm, PriceForm
from .utils import DealFilter

# -----------------------------------------------
# CREATE VIEWS
# -----------------------------------------------
class CustomCreateView(CreateView):
    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        i = {}
        tenant = tenant_from_request(self.request)
        i = {'tenant': tenant.id, 'deal': self.kwargs.get('deal_id')}
        return i.copy()


class CreateCustomer(CustomCreateView):
    model = Customer
    form_class = CustomerForm

    def get_success_url(self):
        return reverse('deals:new-deal', kwargs={'customer_id': self.object.id})


class CreateShutterItem(CustomCreateView):
    form_class = ShutterForm
    model = Shutter

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the items
        # context['deal_id'] = self.kwargs.get('deal_id')
        context['items'] = Shutter.objects.filter(deal_id=self.kwargs.get('deal_id'))
        return context

    def get_success_url(self):
        return reverse('deals:create-shutter-item', kwargs={'deal_id': self.object.deal_id})


def new_deal(request, customer_id):
    tenant = tenant_from_request(request)
    deal = Deal.objects.create(tenant_id=tenant.id, agent=request.user, measured_by=request.user, customer_id=customer_id)
    price = Price.objects.create(deal_id=deal.id, tenant_id=tenant.id)
    material = Material.objects.create(deal_id=deal.id, tenant_id=tenant.id)
    return redirect(reverse('deals:create-shutter-item', kwargs={'deal_id': deal.id}))


def deal_specs(request, deal_id):
    shutter = Shutter.objects.filter(deal_id=deal_id)
    price = Price.objects.get(deal_id=deal_id)
    material = Material.objects.get(deal_id=deal_id)

    # calculate deal totals
    subtotal = round(sum(i.total_price() for i in shutter), 2)
    price.subtotal = subtotal
    price.tax = (price.subtotal * price.tax_rate) if price.add_tax else 0
    price.credit_card_fee = (price.subtotal * price.credit_card_fee_rate) if price.payment_method_id == 3 else 0
    price.total = price.subtotal + price.tax + price.credit_card_fee
    price.balance = price.total - price.down_payment
    price.save()

    # calculate materials needed
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

    return redirect(reverse('deals:deal-summary', kwargs={'pk': deal_id}))


# -----------------------------------------------
# EDIT VIEWS
# -----------------------------------------------
class UpdateCustomer(UpdateView):
    model = Customer
    form_class = CustomerForm

    def get_success_url(self):
        return reverse('deals:deal-summary', kwargs={'pk': self.kwargs.get('deal_id')})


class UpdateShutterItem(UpdateView):
    model = Shutter
    form_class = ShutterForm

    def get_success_url(self):
        return reverse('deals:deal-specs', kwargs={'deal_id': self.kwargs.get('deal_id')})


class UpdateDeal(UpdateView):
    model = Deal
    form_class = DealForm

    def get_form_kwargs(self):
        tenant = tenant_from_request(self.request)
        kwargs = super().get_form_kwargs()
        kwargs['tenant'] = tenant.id
        return kwargs

    def get_success_url(self):
        return reverse('deals:deal-summary', kwargs={'pk': self.kwargs.get('pk')})


class UpdatePrice(UpdateView):
    model = Price
    form_class = PriceForm

    def get_success_url(self):
        return reverse('deals:deal-specs', kwargs={'deal_id': self.kwargs.get('pk')})


class UpdateDealStatus(UpdateView):
    model = Deal
    fields = ['status']
    template_name = 'deals/deal_confirm_status.html'

    def get_initial(self): # set deal status from URL pattern
        i = {}
        i = {'status': self.kwargs.get('status')}
        return i.copy()

    def get_success_url(self):
        return reverse('core:home')


def set_style_default(request):
    id_list = request.POST.getlist('item_list')
    items = Shutter.objects.filter(id__in=id_list)

    for item in items:
        item.default_style = True
        item.save()

    return redirect(reverse('deals:update-shutter-style', kwargs={'pk': id_list[0]}))


class UpdateShutterStyle(UpdateView):
    model = Shutter
    fields = ['deal', 'finish', 'stain', 'color', 'louver', 'tilt_rod', 'trim_style', 'hinge_color']
    template_name = 'shutters/shutter_style_form.html'

    def form_valid(self, form):
        self.object.default_style = False
        self.object = form.save()

        # update remaining deal items
        items = Shutter.objects.filter(default_style=True)

        for item in items:
            item.finish = self.object.finish
            item.stain = self.object.stain
            item.color = self.object.color
            item.louver = self.object.louver
            item.tilt_rod = self.object.tilt_rod
            item.trim_style = self.object.trim_style
            item.hinge_color = self.object.hinge_color
            item.default_style = False
            item.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('deals:deal-summary', kwargs={'pk': self.get_object().deal_id})


# -----------------------------------------------
# DELETE VIEWS
# -----------------------------------------------
class DeleteItem(DeleteView):
    model = Shutter

    def get_success_url(self):
        return reverse('deals:deal-specs', kwargs={'deal_id': self.get_object().deal_id})


# -----------------------------------------------
# DISPLAY VIEWS
# -----------------------------------------------
@login_required
def deal_list(request, status):
    if status == 'Deleted':
        q = Deal.objects.filter(status='Deleted')
    elif status == 'Completed':
        q = Deal.objects.filter(status='Completed')
    else:
        q = Deal.objects.filter(status='Active')

    filter = DealFilter(request.GET, queryset=q)

    return render(request, 'core/home.html', {'filter': filter, 'status': status})


# -----------------------------------------------
# SUMMARY VIEW
# -----------------------------------------------
def deal_summary(request, pk):
    deal = Deal.objects.get(id=pk)
    price = Price.objects.get(deal_id=pk)
    customer = Customer.objects.get(id=deal.customer_id)
    shutter = Shutter.objects.filter(deal_id=pk)

    return render(request, 'deals/deal_summary.html', {'customer': customer, 'deal': deal, 'items': shutter, 'price': price})
