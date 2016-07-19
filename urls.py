from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
	url(r'^$', views.index, name='index'),
    	url(r'^(?P<page_number>[0-9]+)$', views.index, name='index'),
    	url(r'^archives/$', views.archives, name='archives'),
    	url(r'^archives/(?P<page_number>[0-9]+)$', views.archives, name='archives'),
    	url(r'^category/(?P<name>[\w]+)/(?P<page_number>[0-9]+)/$', views.category, name='category'),
    	url(r'^category/(?P<name>[\w]+)$', views.category, name='category'),
    	url(r'^article/(?P<title>[\w]+)$', views.article, name='article'),

    	url(r'^tag/(?P<title>[\w]+)$', views.tag, name='tag'),
    	url(r'^tag/(?P<name>[\w]+)/(?P<page_number>[0-9]+)/$', views.tag, name='tag'),
    url(r'^tags$', views.tags, name='tags'),
]