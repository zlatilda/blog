from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *
app_name = 'blog'

urlpatterns = [
    url(r'^home/$', index, name='index'),
    url(r'registration/', signup, name='signup'),
    url(r'create-profile/', create_profile, name='create_profile'),
    url(r'^post/(?P<post_pk>\d+)/$', post_detail, name='post_detail'),
    url(r'result/', search, name="search"),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
