from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/$', views.show_board),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail),
    url(r'^writepost/$', views.write_post, name='writepost'),
]
