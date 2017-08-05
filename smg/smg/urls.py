from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('authentication.urls', namespace='auth')),
    url(r'^ooo/', include('out_of_office.urls', namespace='ooo')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
