from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/accounts/login/')),  # Redirect to login page
    path('admin/login/', RedirectView.as_view(url='/accounts/login/')),  # Redirect admin login to allauth login
    path('admin/', admin.site.urls),  # Default admin URL
    path('accounts/', include('allauth.urls')),  # Include allauth URLs
    path('documents/', include('documents.urls', namespace='documents')),
    path('api/', include('documents.urls_api', namespace='documents-api')),
    path('mfa/', include(('allauth.mfa.urls', 'mfa'), namespace='allauth-mfa')),  # Include MFA URLs with unique namespace
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
