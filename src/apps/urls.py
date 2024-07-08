from django.urls import re_path, include

from apps.accounts.urls import v1_urlpatterns as v1_accounts_urls
from apps.bicycles.urls import router as bicycles_router


v1_urlpatterns = [
    re_path(r'', include((v1_accounts_urls, 'accounts'))),
    re_path(r'', include((bicycles_router.urls, 'rentals')))
]