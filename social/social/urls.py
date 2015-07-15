from django.conf.urls import include, url
from django.contrib import admin
from social_list import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'social.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^$', views.home)
]
