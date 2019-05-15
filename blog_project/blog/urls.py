from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *
from . import views as core_view
from django.urls import path, include
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
    url(r'profile/(?P<pk>[-\w]+)/', get_user_profile, name='get_user_profile'),
    url('edit/post/(?P<pk>[-\w]+)/', edit_post, name='edit_post'),
    url(r'user-settings/', user_settings, name='user_settings'),
    url(r'change-password/', change_password, name='change_password'),
    path('favourite/post/<int:pk>', AddToFavorite.as_view(), name='add-favourite'),
    path('delete-favourite/post/<int:pk>', RemoveFromFavorite.as_view(), name='remove-favourite'),
    url(r'favourites/(?P<pk>[-\w]+)/', get_user_favourites, name='get_user_favourites'),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
