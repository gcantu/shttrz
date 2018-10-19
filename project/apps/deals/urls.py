from django.urls import path, include
from . import views

app_name = 'deals'

urlpatterns = [
    path('add_customer', views.add_customer, name='add-customer'),
    path('add_item/<int:pk>', views.add_deal_item, name='add-deal-item'),
    path('add_price/<int:pk>', views.add_deal_price, name='add-deal-price'),
    path('add_material/<int:pk>', views.add_material, name='add-material'),
    path('edit_customer/<int:pk>', views.edit_customer, name='edit-customer'),
    path('edit_deal/<int:pk>', views.edit_deal_info, name='edit-deal-info'),
    path('edit_item/<int:pk>', views.edit_deal_item, name='edit-deal-item'),
    path('edit_pricing/<int:pk>', views.edit_deal_price, name='edit-deal-price'),
    path('summary/<int:pk>', views.deal_summary, name='deal-summary'),
]
