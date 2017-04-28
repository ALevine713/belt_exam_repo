from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^add_quote$', views.add_quote),
    url(r'^add_favorite/(?P<quote_id>\d+)$', views.add_favorite),
    url(r'^remove_favorite/(?P<quote_id>\d+)$', views.remove_favorite),
    url(r'^users/(?P<user_id>\d+)$', views.posted_by),
]
