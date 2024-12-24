from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    
    # Django-allauth URLs
    path('accounts/', include('allauth.urls')),
    
    # Local apps URLs
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('banking/', include('banking.urls', namespace='banking')),
    path('budgets/', include('budgets.urls', namespace='budgets')),
    path('transactions/', include('transactions.urls', namespace='transactions')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
