from django.urls import path, include
from . import views

app_name = 'reports'

urlpatterns = [
    path('proposal/<int:pk>', views.proposal_report, name='proposal-report'),
    path('manufacturing_report/<int:pk>', views.manufacturing_report, name='manufacturing-report'),
]
