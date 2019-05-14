from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *
from . import views as core_view
app_name = 'blog'

urlpatterns = [
    url(r'^home/$', index, name='index'),
    url(r'registration/', signup, name='signup'),
    url(r'create-profile/', create_profile, name='create_profile'),
    url(r'^post/(?P<post_pk>\d+)/$', post_detail, name='post_detail'),
    url(r'result/', search, name="search"),
    url(r'^(?P<pk>[-\w]+)/delete/$', comment_delete, name='comment_delete'),
    url(r'(?P<slug>[-\w]+)/like/', core_view.PostLikeToggle.as_view(), name="like-toggle"),
    url(r'create-new/', post_new, name='create-post'),
    url('delete/post/(?P<pk>[-\w]+)/', post_delete, name='post-delete'),
    url(r'^ordered/(?P<variable>[-\w]+)/', order_by_params, name='order_by_params'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
