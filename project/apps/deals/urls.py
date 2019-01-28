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
    path('delete_shutter_item/<int:pk>', views.DeleteShutterItem.as_view(), name='delete-shutter-item'),
    path('update_status/<int:pk>/<status>', views.UpdateDealStatus.as_view(), name='update-deal-status'),

    path('set_blinds_style_default', views.set_blinds_style_default, name='blind-style-default'),
    path('update_blind_style/<int:pk>', views.UpdateBlindStyle.as_view(), name='update-blind-style'),

    path('set_shades_style_default', views.set_shades_style_default, name='shade-style-default'),
    path('update_shade_style/<int:pk>', views.UpdateShadeStyle.as_view(), name='update-shade-style'),

    path('<status>', views.deal_list, name='deal-list'),
    path('summary/<int:pk>', views.deal_summary, name='deal-summary'),
    path('summary_items/<int:pk>', views.deal_summary_items, name='deal-summary-items'),

    path('select_product/<int:deal_id>', views.select_product, name='select-product'),
    path('create_blind_item/<int:deal_id>', views.CreateBlindItem.as_view(), name='create-blind-item'),
    path('create_shade_item/<int:deal_id>', views.CreateShadeItem.as_view(), name='create-shade-item'),
    path('create_sunscreen_item/<int:deal_id>', views.CreateSunscreenItem.as_view(), name='create-sunscreen-item'),

    path('update_blind_item/<int:pk>/<int:deal_id>', views.UpdateBlindItem.as_view(), name='update-blinds-item'),
    path('update_shade_item/<int:pk>/<int:deal_id>', views.UpdateShadeItem.as_view(), name='update-shades-item'),
    path('update_sunscreen_item/<int:pk>/<int:deal_id>', views.UpdateSunscreenItem.as_view(), name='update-sunscreens-item'),

    path('delete_blind_item/<int:pk>', views.DeleteBlindItem.as_view(), name='delete-blinds-item'),
    path('delete_shade_item/<int:pk>', views.DeleteShadeItem.as_view(), name='delete-shades-item'),
    path('delete_sunscreen_item/<int:pk>', views.DeleteSunscreenItem.as_view(), name='delete-sunscreens-item'),

    path('history/all', views.deal_history_list, name='deal-history-list'),

    path('location-name-search/', views.location_name_search, name='location-name-search'),
]
