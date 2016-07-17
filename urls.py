from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^(?P<page_number>[0-9]+)$', views.index, name='index'),
    url(r'^archives/$', views.archives, name='archives'),
    url(r'^archives/(?P<page_number>[0-9]+)$', views.archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^blog/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]