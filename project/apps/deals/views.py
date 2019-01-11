from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic import ListView
from tenants.utils import tenant_from_request
from .models import Deal, Price
from shutters.models import Shutter, Material, TrimStyle, TiltRod, HingeColor, Stain
from blinds.models import Blind, FauxWoodStyle
from shades.models import Shade
from sunscreens.models import Sunscreen
from customers.models import Customer
from forms.forms import DealForm, CustomerForm, ShutterForm, PriceForm, BlindForm, ShadeForm, SunscreenForm, DealFilterForm
from .utils import DealFilter
from django.template.defaultfilters import date
import json
from django.http import HttpResponse


def location_name_search(request):
    if request.is_ajax():
        q = request.GET.get('term','').capitalize()
        locations = Shutter.objects.filter(location__startswith=q)
        result = []
        for n in locations:
            result.append(n.location)

        result = list(set(result))
        data = json.dumps(result)

    return HttpResponse(data, 'application/json')

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


class CreateBlindItem(CustomCreateView):
    form_class = BlindForm
    model = Blind
    template_name = "products/product_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Blind.objects.filter(deal_id=self.kwargs.get('deal_id'))
        context['product'] = 'Blinds'
        return context

    def get_success_url(self):
        return reverse('deals:create-blind-item', kwargs={'deal_id': self.object.deal_id})


class CreateShadeItem(CustomCreateView):
    form_class = ShadeForm
    model = Shade
    template_name = "products/product_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Shade.objects.filter(deal_id=self.kwargs.get('deal_id'))
        context['product'] = 'Shades'
        return context

    def get_success_url(self):
        return reverse('deals:create-shade-item', kwargs={'deal_id': self.object.deal_id})


class CreateSunscreenItem(CustomCreateView):
    form_class = SunscreenForm
    model = Sunscreen
    template_name = "products/product_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Sunscreen.objects.filter(deal_id=self.kwargs.get('deal_id'))
        context['product'] = 'Sunscreens'
        return context

    def get_success_url(self):
        return reverse('deals:create-sunscreen-item', kwargs={'deal_id': self.object.deal_id})


def new_deal(request, customer_id):
    tenant = tenant_from_request(request)
    deal = Deal.objects.create(tenant_id=tenant.id, agent=request.user, measured_by=request.user, customer_id=customer_id)
    price = Price.objects.create(deal_id=deal.id, tenant_id=tenant.id)
    material = Material.objects.create(deal_id=deal.id, tenant_id=tenant.id)
    # return redirect(reverse('deals:create-shutter-item', kwargs={'deal_id': deal.id}))
    return redirect(reverse('deals:select-product', kwargs={'deal_id': deal.id}))


def deal_specs(request, deal_id):
    shutter = Shutter.objects.filter(deal_id=deal_id)
    blind = Blind.objects.filter(deal_id=deal_id)
    shade = Shade.objects.filter(deal_id=deal_id)
    sunscreen = Sunscreen.objects.filter(deal_id=deal_id)
    price = Price.objects.get(deal_id=deal_id)
    material = Material.objects.get(deal_id=deal_id)

    # calculate deal totals
    price.shutters_subtotal = round(sum(i.total_price() for i in shutter), 2) if shutter else 0
    price.blinds_subtotal = round(sum(i.total_price() for i in blind), 2) if blind else 0
    price.shades_subtotal = round(sum(i.total_price() for i in shade), 2) if shade else 0
    price.sunscreens_subtotal = round(sum(i.total_price() for i in sunscreen), 2) if sunscreen else 0
    price.subtotal = price.shutters_subtotal + price.blinds_subtotal + price.shades_subtotal + price.sunscreens_subtotal
    price.tax = (price.subtotal * price.tax_rate)
    price.credit_card_fee = (price.subtotal * price.credit_card_fee_rate) if price.payment_method_id == 3 else 0
    price.total = price.subtotal + price.tax + price.credit_card_fee
    price.balance = price.total - price.down_payment
    price.save()

    # calculate materials needed
    if material:
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


class UpdateProductItemView(UpdateView):
    def get_success_url(self):
        return reverse('deals:deal-specs', kwargs={'deal_id': self.kwargs.get('deal_id')})


class UpdateShutterItem(UpdateProductItemView):
    model = Shutter
    form_class = ShutterForm


class UpdateBlindItem(UpdateProductItemView):
    model = Blind
    form_class = BlindForm
    template_name = "products/product_form.html"


class UpdateShadeItem(UpdateProductItemView):
    model = Shade
    form_class = ShadeForm
    template_name = "products/product_form.html"


class UpdateSunscreenItem(UpdateProductItemView):
    model = Sunscreen
    form_class = SunscreenForm
    template_name = "products/product_form.html"


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
    d = Shutter.objects.get(id=id_list[0])
    deal_id = d.deal_id
    dict = request.POST.dict()

    if 'finish' in request.POST:
        f = dict.pop('finish')
        Shutter.objects.filter(id__in=id_list).update(finish=f)

        if f == 'Paint':
            Shutter.objects.filter(id__in=id_list).update(stain='')

    elif 'trim_style' in request.POST:
        ts = dict.pop('trim_style')
        ts = TrimStyle.objects.get(trim_style=ts)
        Shutter.objects.filter(id__in=id_list).update(trim_style=ts)
    elif 'tilt_rod' in request.POST:
        tr = dict.pop('tilt_rod')
        tr = TiltRod.objects.get(tilt_rod=tr)
        Shutter.objects.filter(id__in=id_list).update(tilt_rod=tr)
    elif 'hinge_color' in request.POST:
        hc = dict.pop('hinge_color')
        hc = HingeColor.objects.get(hinge_color=hc)
        Shutter.objects.filter(id__in=id_list).update(hinge_color=hc)
    elif 'stain' in request.POST:
        s = dict.pop('stain')
        s = Stain.objects.get(stain=s)
        Shutter.objects.filter(id__in=id_list).update(stain=s)
    elif 'louver' in request.POST:
        l = dict.pop('louver')
        if l == '2 1/2':
            Shutter.objects.filter(id__in=id_list).update(louver=2.5)
        elif l == '3 1/2':
            Shutter.objects.filter(id__in=id_list).update(louver=3.5)
        else:
            Shutter.objects.filter(id__in=id_list).update(louver=4.5)
    else:
        Shutter.objects.filter(id__in=id_list).update(default_style=True)


    if 'color' in request.POST:
        return redirect(reverse('deals:update-shutter-style', kwargs={'pk': id_list[0]}))
    else:
        return redirect(reverse('deals:deal-summary-items', kwargs={'pk': deal_id}))


def set_blinds_style_default(request):
    id_list = request.POST.getlist('item_list')
    d = Blind.objects.get(id=id_list[0])
    deal_id = d.deal_id
    dict = request.POST.dict()

    if 'faux_wood_style' in request.POST:
        fw = dict.pop('faux_wood_style')
        fw = FauxWoodStyle.objects.get(faux_wood_style=fw)
        Blind.objects.filter(id__in=id_list).update(faux_wood_style=fw)
    else:
        Blind.objects.filter(id__in=id_list).update(default_style=True)

    if 'color_blinds' in request.POST:
        return redirect(reverse('deals:update-blind-style', kwargs={'pk': id_list[0]}))
    else:
        return redirect(reverse('deals:deal-summary-items', kwargs={'pk': deal_id}))


class UpdateShutterStyle(UpdateView):
    model = Shutter
    fields = ['deal', 'color']
    template_name = 'shutters/shutter_style_form.html'

    def form_valid(self, form):
        self.object.default_style = False
        self.object = form.save()

        # update remaining deal items
        items = Shutter.objects.filter(default_style=True)

        for item in items:
            item.color = self.object.color
            item.default_style = False
            item.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('deals:deal-summary-items', kwargs={'pk': self.get_object().deal_id})


class UpdateBlindStyle(UpdateView):
    model = Blind
    fields = ['deal', 'color']
    template_name = 'products/product_style_form.html'

    def form_valid(self, form):
        self.object.default_style = False
        self.object = form.save()

        # update remaining deal items
        items = Blind.objects.filter(default_style=True)

        for item in items:
            item.color = self.object.color
            item.default_style = False
            item.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('deals:deal-summary-items', kwargs={'pk': self.get_object().deal_id})


# -----------------------------------------------
# DELETE VIEWS
# -----------------------------------------------
class DeleteItemView(DeleteView):
    def get_success_url(self):
        return reverse('deals:deal-specs', kwargs={'deal_id': self.get_object().deal_id})

class DeleteShutterItem(DeleteItemView):
    model = Shutter

class DeleteBlindItem(DeleteItemView):
    model = Blind
    template_name = 'products/product_confirm_delete.html'

class DeleteShadeItem(DeleteItemView):
    model = Shade
    template_name = 'products/product_confirm_delete.html'

class DeleteSunscreenItem(DeleteItemView):
    model = Sunscreen
    template_name = 'products/product_confirm_delete.html'


# -----------------------------------------------
# DISPLAY VIEWS
# -----------------------------------------------
@login_required
def deal_list(request, status):
    tenant = tenant_from_request(request)

    if status == 'Deleted':
        q = Deal.objects.filter(tenant_id=tenant.id, status='Deleted')
    elif status == 'Completed':
        q = Deal.objects.filter(tenant_id=tenant.id, status='Completed')
    else:
        q = Deal.objects.filter(tenant_id=tenant.id, status='Active')

    filter = DealFilter(request.GET, queryset=q)

    return render(request, 'core/home.html', {'filter': filter, 'status': status})


@login_required
def deal_history_list(request):
    tenant = tenant_from_request(request)
    all_deals = Deal.objects.filter(tenant_id=tenant.id, status='Completed')
    years = list(set([(i.created_date.year, str(i.created_date.year)) for i in all_deals]))
    # months = list(set([date(i.created_date, 'F') for i in all_deals]))
    months = list(set([(i.created_date.month, date(i.created_date, 'F')) for i in all_deals]))
    form = DealFilterForm(years=years, months=months)
    deals = None
    dict = request.POST.dict()

    if 'year' in request.POST and 'month' in request.POST:
        y = dict.pop('year')
        m = dict.pop('month')
        form = DealFilterForm(years=years, months=months, initial={'year': y, 'month': m})

        if y == 'All' and m == 'All':
            deals = Deal.objects.filter(tenant_id=tenant.id, status='Completed').order_by('created_date')
        elif y == 'All':
            deals = Deal.objects.filter(tenant_id=tenant.id, status='Completed', created_date__month=m).order_by('created_date')
        elif m == 'All':
            deals = Deal.objects.filter(tenant_id=tenant.id, status='Completed', created_date__year=y).order_by('created_date')
        else:
            deals = Deal.objects.filter(tenant_id=tenant.id, status='Completed', created_date__year=y, created_date__month=m).order_by('created_date')

    return render(request, 'deals/deal_history.html', {'form': form, 'deals': deals})


# -----------------------------------------------
# SUMMARY VIEW
# -----------------------------------------------
def deal_summary(request, pk):
    deal = Deal.objects.get(id=pk)
    price = Price.objects.get(deal_id=pk)
    customer = Customer.objects.get(id=deal.customer_id)

    return render(request, 'deals/deal_summary.html', {'customer': customer, 'deal': deal, 'price': price})


def deal_summary_items(request, pk):
    deal = Deal.objects.get(id=pk)
    shutter = Shutter.objects.filter(deal_id=pk).order_by('shutter_type_id')
    blind = Blind.objects.filter(deal_id=pk).order_by('blind_type_id')
    shade = Shade.objects.filter(deal_id=pk).order_by('shade_type_id')
    sunscreen = Sunscreen.objects.filter(deal_id=pk).order_by('sunscreen_type_id')

    product_list = [blind, shade, sunscreen]

    return render(request, 'deals/deal_summary_items.html', {'deal': deal, 'items': shutter, 'product_list': product_list})


# -----------------------------------------------
# OTHER PRODUCTS
# -----------------------------------------------
def select_product(request, deal_id):
    return render(request, 'products/select_product.html', {'deal_id': deal_id})
