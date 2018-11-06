from django.conf.urls import url,include
from django.views.generic import TemplateView
from book import views


urlpatterns = [
   	url(r'^profile', views.profile, name='profile' ),
    url(r'^bookid/(?P<book_id>\w{0,50})/$', views.book,name='bookid'),
    url(r'^preregister/(?P<b_id>\w{0,50})/$',views.preregister,name='preregister'),
    url(r'^donepreregister/$',views.done_preregister,name='allbooks'),
    url(r'^comment/(?P<book_id>\w{0,50})/$',views.post_comment,name='post'),
    url(r'^tables/$',views.tables,name= 'table'),
    url(r'^settings/$',views.setting, name= 'settings'),
    url(r'^update_settings/$',views.update_settings, name= 'u_settings'),
    url(r'^cancelprebook/(?P<b_id>\w{0,50})/$',views.cancelprebook, name= 'cancel'),
    ]
