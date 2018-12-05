from django.urls import path, include
from . import views

app_name = 'deals'

urlpatterns = [
    path('create_customer', views.CreateCustomer.as_view(), name='create-customer'),
    path('create_shutter_item/<int:deal_id>', views.CreateShutterItem.as_view(), name='create-shutter-item'),
    path('new_deal/<int:customer_id>', views.new_deal, name='new-deal'),
    path('deal_specs/<int:deal_id>', views.deal_specs, name='deal-specs'),
    path('update_customer/<int:pk>/<int:deal_id>', views.UpdateCustomer.as_view(), name='update-customer'),
    path('update_shutter_item/<int:pk>/<int:deal_id>', views.UpdateShutterItem.as_view(), name='update-shutter-item'),
    path('update_deal/<int:pk>', views.UpdateDeal.as_view(), name='update-deal'),
    path('update_pricing/<int:pk>', views.UpdatePrice.as_view(), name='update-price'),
    path('set_style_default', views.set_style_default, name='style-default'),
    path('update_shutter_style/<int:pk>', views.UpdateShutterStyle.as_view(), name='update-shutter-style'),
    path('delete_shutter_item/<int:pk>', views.DeleteItem.as_view(), name='delete-shutter-item'),
    path('update_status/<int:pk>/<status>', views.UpdateDealStatus.as_view(), name='update-deal-status'),
    path('<status>', views.deal_list, name='deal-list'),
    path('summary/<int:pk>', views.deal_summary, name='deal-summary'),
    path('summary_items/<int:pk>', views.deal_summary_items, name='deal-summary-items'),
]
