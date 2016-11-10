from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from filebrowser_rest import views

urlpatterns = [
    url(r'^file$', views.file_operate, name='file'),
    url(r'^directory$', views.dir_operate, name='directory'),
    url(r'^cpmv$', views.cpmv, name='cpmv'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
