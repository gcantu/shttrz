from django.forms import ModelForm
from deals.models import Deal, Price
from customers.models import Customer
from shutters.models import Shutter


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class DealForm(ModelForm):
    class Meta:
        model = Deal
        fields = '__all__'


class PriceForm(ModelForm):
    class Meta:
        model = Price
        fields = '__all__'


class ShutterForm(ModelForm):
    class Meta:
        model = Shutter
        fields = '__all__'
