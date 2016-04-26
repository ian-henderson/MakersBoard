from django.conf.urls import url

from .views import (
    user_list,
    user_create,
    user_detail,
    user_update,
    user_delete,
    user_login,
    user_logout
)


urlpatterns = [
    url(r'^$', user_list, name='list'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^create/$', user_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', user_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', user_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', user_delete, name='delete'),
]
