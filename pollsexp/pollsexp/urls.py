from django.conf.urls import include, url
from django.contrib import admin
from polls import urls as polls_urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'pollsexp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include(polls_urls))
]
