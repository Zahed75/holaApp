from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auths.urls')),
    path('',include('auths.urls')),
    path('',include('outlet.urls')),
    path('',include('order.urls')),
    path('',include('products.urls')),
    path('',include('payment.urls')),
    path('',include('reporting.urls')),
    path('',include('settings.urls')),
    path('',include('settings.urls')),
    path('',include('category.urls')),
    path('',include('customer.urls')),
    path('',include('discount.urls')),


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)