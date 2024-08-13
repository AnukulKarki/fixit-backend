
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/',include('registration.urls')),
    path('api/job/', include('jobposting.urls')),
    path('api/worker/gig/',include('gig.urls')),
    path('api/worker/proposal/',include('proposal.urls')),
    path('api/category/',include('category.urls')),
    path('api/work/', include('currentwork.urls')),
    path('api/hire/', include('gighire.urls')),
    path('api/admin/brand/', include('brand.urls')),
    path('api/admin/blacklist/', include('blacklist.urls')),
    path('api/message/', include('message.urls')),
    path('api/badge/', include('badge.urls')),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)

