from django.forms import ModelForm
from deals.models import Deal, Price
from customers.models import Customer
from shutters.models import Shutter
from tenants.utils import tenant_from_request
from django.contrib.auth import get_user_model

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


class PriceForm(ModelForm):
    class Meta:
        model = Price
        exclude = ['deal', 'tenant', 'shutters_subtotal', 'blinds_subtotal', 'shades_subtotal', 'sunscreens_subtotal', 'subtotal', 'tax', 'credit_card_fee', 'total', 'balance']


class ShutterForm(ModelForm):
    class Meta:
        model = Shutter
        exclude = ['frame_style', 'product', 'default_style']
