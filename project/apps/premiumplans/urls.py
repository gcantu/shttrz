from django.urls import path, include
from . import views

app_name = 'premiumplans'

urlpatterns = [
    path('select_product/<int:deal_id>', views.select_product, name='select-product'),
    path('create_blind_item/<int:deal_id>', views.CreateBlindItem.as_view(), name='create-blind-item'),
    path('create_shade_item/<int:deal_id>', views.CreateShadeItem.as_view(), name='create-shade-item'),
    path('create_sunscreen_item/<int:deal_id>', views.CreateSunscreenItem.as_view(), name='create-sunscreen-item'),
    path('update_blind_item/<int:pk>/<int:deal_id>', views.UpdateBlindItem.as_view(), name='update-blind-item'),
    path('update_shade_item/<int:pk>/<int:deal_id>', views.UpdateShadeItem.as_view(), name='update-shade-item'),
    path('update_sunscreen_item/<int:pk>/<int:deal_id>', views.UpdateSunscreenItem.as_view(), name='update-sunscreen-item'),
    path('delete_blind_item/<int:pk>', views.DeleteBlindItem.as_view(), name='delete-blind-item'),
    path('delete_shade_item/<int:pk>', views.DeleteShadeItem.as_view(), name='delete-shade-item'),
    path('delete_sunscreen_item/<int:pk>', views.DeleteSunscreenItem.as_view(), name='delete-sunscreen-item'),
    path('p/summary/<int:pk>', views.deal_summary, name='deal-summary'),

]
