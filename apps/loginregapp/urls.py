from django.conf.urls import url
from . import views           
urlpatterns = [
	url(r'^main$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$',views.success),
    url(r'^logout$',views.logout),
    url(r'^wish_items/create$',views.additem),
    url(r'^createprocess$',views.createprocess),
    url(r'^wish_items/(?P<id>\d+)$',views.showitem),
    url(r'^addwishlistprocess/(?P<id>\d+)$',views.addwishlistprocess),
    url(r'^removewishlist/(?P<id>\d+)$',views.removewishlist),
    url(r'^delete/(?P<id>\d+)$',views.delete)

]
