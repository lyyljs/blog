from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from .models import *
import datetime,time,copy

PAGE_SIZE = 8
'''
获取头部信息（分类信息）
'''
def getHeaderInfo():
	category_list = Category.objects.all()
	return {'category_list':category_list}
'''
获取右侧栏信息
'''
def getRightInfo():
	article_count = Article.objects.count()
	category_count = Category.objects.count()
	tag_count = Tag.objects.count()
	return {'article_count':article_count,'category_count':category_count,'tag_count':tag_count}
'''
获取分页信息
'''
def getPageInfo(page_number):
	content_dict = {}
	try:
		page_number = int(page_number)
	except ValueError:
		page_number = 1
	start_pos = (page_number - 1) * PAGE_SIZE
	end_pos = start_pos + PAGE_SIZE

	total_pages = Article.objects.all().count()
	if (total_pages/PAGE_SIZE == total_pages//PAGE_SIZE):
		total_pages //= PAGE_SIZE
	else:
		total_pages = total_pages//PAGE_SIZE + 1

	if (page_number < total_pages - 1 and page_number > 2):
		l_range = range(page_number-1,page_number+2)
	elif (page_number > 2):
		l_range = range(page_number-1,total_pages+1)
	elif (page_number < total_pages - 1):
		l_range = range(1,page_number+2)
	else:
		l_range = range(1,total_pages+1)

	content_dict['start_pos'] = start_pos
	content_dict['end_pos'] = end_pos
	content_dict['l_range'] = l_range
	content_dict['page_number'] = page_number
	content_dict['total_pages'] = total_pages
	return content_dict
'''
blog列表
'''
def index(request,page_number=1):
	content_dict = getPageInfo(page_number)

	latest_blog_list = Article.objects.filter(is_draft=False).order_by('-create_time')[content_dict['start_pos']:content_dict['end_pos']]
	for blog in latest_blog_list:
		blog.comment_counts = blog.comment_set.all().count()
	
	content_dict['this_url'] = 'blog:index'
	content_dict['latest_blog_list'] = latest_blog_list
	content_dict.update(getHeaderInfo())
	content_dict.update(getRightInfo())

	return render(request, 'blog/index.html', content_dict)
'''
归档
'''
def archives(request,page_number=1):
	content_dict = getPageInfo(page_number)

	latest_blog_list = Article.objects.filter(is_draft=False).order_by('-create_time')[content_dict['start_pos']:content_dict['end_pos']]
	node_list = []
	year_node = latest_blog_list[0]
	year_node.year = int(latest_blog_list[0].create_time.__str__()[:4])
	year_node.is_blog = False
	node_list.append(year_node)
	for blog in latest_blog_list:
		blog.is_blog = True
		blog_create_year = int(blog.create_time.__str__()[:4])
		if (blog_create_year != year_node.year):
			year_node = copy.deepcopy(year_node)
			year_node.year = blog_create_year
			node_list.append(year_node)
		node_list.append(blog)

	content_dict['this_url'] = 'blog:archives'
	content_dict['node_list'] = node_list
	content_dict.update(getHeaderInfo())
	content_dict.update(getRightInfo())
	return render(request, 'blog/archive.html', content_dict)

class DetailView(generic.DetailView):
    model = Article
    template_name = 'blog/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Article.objects.filter(pub_date__lte=timezone.now())

class CategoryView(generic.ListView):
	template_name = 'blog/category.html'
	context_object_name = 'category_blog_list'
	def get_queryset(self):
		return Article.objects.all()