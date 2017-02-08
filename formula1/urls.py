from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from socialhub.views import getposts


api_patterns = [
    # API
    url(r'^auth/', include('authentication.urls')),
    url(r'^premio/', include('premio.urls')),
    url(r'^store/', include('store.urls')),

]


urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_patterns)),
    url(r'^social-hub/', include('socialhub.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

