from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_api import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^services$', views.service_list, name='services'),
    url(r'^containers$', views.container_list, name='containers'),
    url(r'^projects$', views.project_list, name='projects'),
    url(r'^projects/(?P<pro>\S+)$', views.project, name='project'),
    url(r'^service', views.service, name='service'),
    url(r'^container', views.container, name='container'),
    url(r'^log$', views.log, name='logs'),
    url(r'^monitor$', views.monitor, name='monitor'),
    url(r'^network$', views.network, name='network'),
    url(r'^yaml$', views.yaml, name='yaml'),
    url(r'^images$', views.images, name='images'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
