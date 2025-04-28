# budget_tracker/urls.py (main project URLs)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('finance.urls')),  # Includes the finance app URLs
]
