
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('deals/', include('deals.urls')),
    path('reports/', include('reports.urls')),
    path('dashboard/', include('dashboard.urls')),
]
