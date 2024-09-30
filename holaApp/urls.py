from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('admin/', admin.site.urls),
    path('auth/', include('auths.urls')),
    path('auth/',include('auths.urls')),
    path('outlet/',include('outlet.urls')),
    path('order/',include('order.urls')),
    path('products/',include('products.urls')),
    path('payment/',include('payment.urls')),
    path('reporting/',include('reporting.urls')),
    path('settings/',include('settings.urls')),
    path('category/',include('category.urls')),
    path('customer/',include('customer.urls')),
    path('discount/',include('discount.urls')),
    path('wishlist/',include('wishlist.urls')),


]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)