from django.forms import ModelForm
from deals.models import Deal, Price
from customers.models import Customer
from shutters.models import Shutter
from blinds.models import Blind
from shades.models import Shade
from sunscreens.models import Sunscreen
from tenants.utils import tenant_from_request
from django.contrib.auth import get_user_model
from django.forms.widgets import TextInput
from django.forms import fields
from django import forms

User = get_user_model()

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class DealForm(ModelForm):
    class Meta:
        model = Deal
        exclude = ['is_deleted', 'customer', 'status', 'tenant']

    def __init__(self, *args, **kwargs):
        self.tenant = kwargs.pop('tenant')
        super(DealForm, self).__init__(*args, **kwargs)
        self.fields['agent'].queryset = User.objects.filter(tenant_id=self.tenant).exclude(is_superuser=True)
        self.fields['measured_by'].queryset = User.objects.filter(tenant_id=self.tenant).exclude(is_superuser=True)


class PercentageInput(TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        try:
            value = float(value)
            value *= 100
        except ValueError:
            pass
        return super(PercentageInput, self).render(name, value, attrs)

class FormPercentageField(fields.FloatField):
    widget = PercentageInput

    def to_python(self, value):
        value = super(FormPercentageField, self).to_python(value)
        return value / 100


class PriceForm(ModelForm):
    tax_rate = FormPercentageField()
    credit_card_fee_rate = FormPercentageField()

    class Meta:
        model = Price
        exclude = ['deal', 'tenant', 'subtotal', 'tax', 'credit_card_fee', 'total', 'balance', 'add_tax', 'shutters_subtotal', 'blinds_subtotal', 'shades_subtotal', 'sunscreens_subtotal']


class ShutterForm(ModelForm):
    class Meta:
        model = Shutter
        exclude = ['product', 'default_style']


class BlindForm(ModelForm):
    class Meta:
        model = Blind
        exclude = ['price_per_sq_ft']
        # fields = '__all__'


class ShadeForm(ModelForm):
    class Meta:
        model = Shade
        exclude = ['price_per_sq_ft']
        # fields = '__all__'


class SunscreenForm(ModelForm):
    class Meta:
        model = Sunscreen
        exclude = ['price_per_sq_ft']
        # fields = '__all__'


def getKey(item):
    return item[0]

class DealFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        years = sorted(kwargs.pop('years', None), key=getKey)
        months = sorted(kwargs.pop('months', None), key=getKey)
        all = ('All', 'All')
        months.insert(0, all)
        years.insert(0, all)
        super(DealFilterForm, self).__init__(*args, **kwargs)
        if years:
            self.fields['year'] = forms.ChoiceField(choices=years)

        if months:
            self.fields['month'] = forms.ChoiceField(choices=months)
