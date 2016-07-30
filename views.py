from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from .models import *
import datetime,time,copy

PAGE_SIZE = 2
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

'''
文章详情
'''
def article(request,title):
	content_dict = {}
	article = Article.objects.get(title=title)
	comments = article.comment_set.all()
	tags = article.tags.all()
	article.comment_counts = comments.count()
	next_blog = Article.objects.filter(create_time__lt=article.create_time).filter(is_draft=False).order_by('-create_time')[:1]
	prev_blog = Article.objects.filter(create_time__gt=article.create_time).filter(is_draft=False).order_by('create_time')[:1]

	content_dict['this_url'] = 'blog:article'
	content_dict['article'] = article
	try:
		content_dict['next_blog'] = next_blog[0]
	except Exception as e:
		content_dict['next_blog'] = next_blog

	try:
		content_dict['prev_blog'] = prev_blog[0]
	except Exception as e:
		content_dict['prev_blog'] = prev_blog

	content_dict['comments'] = comments
	content_dict['tags'] = tags
	content_dict.update(getHeaderInfo())
	content_dict.update(getRightInfo())
	return render(request, 'blog/article.html', content_dict)

'''
分类
'''
def category(request,name,page_number=1):
	content_dict = getPageInfo(page_number)
	category = Category.objects.get(category_name=name)
	node_list = Article.objects.filter(is_draft=False).filter(category=category).order_by('-create_time')[content_dict['start_pos']:content_dict['end_pos']]

	content_dict['this_url'] = 'blog:category'
	content_dict['param'] = name
	content_dict['category'] = category
	content_dict['node_list'] = node_list
	content_dict.update(getHeaderInfo())
	content_dict.update(getRightInfo())
	return render(request, 'blog/category.html', content_dict)

'''
生成标签云的字体大小或颜色值
'''
def generateSizeList(min_value,max_value,groups,acc):
	if (groups <= 2):
		return [min_value,max_value]
	else:
		step = (max_value-min_value)/(groups-1)
		value = min_value
		result = []
		while value<max_value:
			result.append(round(value,acc))
			value += step
		result.append(max_value)
		return result

'''
获取标签云
'''
def get_tag_cloud(tags):
	tag_ref_count_set = set()
	max_ref_count = 0
	min_ref_count = Article.objects.all().count()
	for tag in tags:
		tag.ref_count = tag.article_set.all().count()
		tag_ref_count_set.add(tag.ref_count)
		if (tag.ref_count > max_ref_count):
			max_ref_count = tag.ref_count
		if (tag.ref_count < min_ref_count):
			min_ref_count = tag.ref_count

	step_diff = max_ref_count - min_ref_count
	groups = len(tag_ref_count_set)
	sorted_tag_refs = list(tag_ref_count_set)
	sorted_tag_refs.sort()

	MIN_FONT_SIZE = 12
	MAX_FONT_SIZE = 30
	MIN_COLOR_VAL = 17
	MAX_COLOR_VAL = 204
	FONT_SIZES = generateSizeList(MIN_FONT_SIZE, MAX_FONT_SIZE, groups, 1)
	COLORS = generateSizeList(MIN_COLOR_VAL, MAX_COLOR_VAL, groups, 0)
	COLORS.reverse()
	for tag in tags:
		index = sorted_tag_refs.index(tag.ref_count)
		tag.font_size = FONT_SIZES[index]
		color = str(COLORS[index])
		tag.color = 'rgb(' + color + ',' + color + ',' + color + ')'
	return {'tags':tags}

'''
标签
'''
def tag(request,name,page_number=1):
	content_dict = getPageInfo(page_number)
	tag = Tag.objects.get(tag_name=name)
	node_list = Article.objects.filter(is_draft=False, tags=tag).order_by('-create_time')[content_dict['start_pos']:content_dict['end_pos']]

	content_dict['this_url'] = 'blog:tag'
	content_dict['param'] = name
	content_dict['tag'] = tag
	content_dict['node_list'] = node_list
	content_dict.update(getHeaderInfo())
	content_dict.update(getRightInfo())
	return render(request, 'blog/tag.html', content_dict)

'''
标签列表
'''
def tags(request):
	content_dict = {}
	tags = Tag.objects.all()

	content_dict.update(get_tag_cloud(tags))
	content_dict.update(getHeaderInfo())
	content_dict.update(getRightInfo())
	return render(request, 'blog/tags.html', content_dict)