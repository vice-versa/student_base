from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import os
DIRNAME = os.path.dirname(__file__)

urlpatterns = patterns("",
    (r'', include('technics4me.urls')),
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^manage/', include('lfs.manage.urls')),
)


urlpatterns += patterns("",
    (r'^admin/', include(admin.site.urls)),

    (r'^assets/admin_tools/(?P<path>.*)$', 'django.views.static.serve',
     { 'document_root': os.path.join(DIRNAME, 'contrib', 'admin_tools','media','admin_tools')}),
    (r'^assets/(?P<path>.*)$', 'django.views.static.serve',
     { 'document_root': settings.MEDIA_ROOT }),
)
