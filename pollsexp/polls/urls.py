from django.conf.urls import include, url
from polls import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'pollsexp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.home, name="Home"),
    url(r'^(\d+)/$',views.result, name="Result"),
    url(r'^(\d+)/vote$',views.vote, name="Vote"),
    url(r'^(\d+)/options/$',views.options, name="Options"),
]
