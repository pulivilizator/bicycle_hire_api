from django.contrib import admin
from django.urls import path, re_path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.urls import v1_urlpatterns
from apps.accounts.urls import router as password_reset_router

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^v1/', include(v1_urlpatterns)),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
