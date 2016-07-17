import datetime,time
from django.utils import timezone
from django.db import models

class User(models.Model):
	user_name = models.CharField(max_length=50)
	user_password = models.CharField(max_length=50)
	user_phone = models.CharField(max_length=30)
	user_email = models.EmailField()
	create_date = models.DateTimeField('create_date', auto_now_add=True)
	update_date = models.DateTimeField('update_date', auto_now_add=True)
	def __str__(self):
		return self.user_name

class Category(models.Model):
	category_name = models.CharField(max_length=50)
	def __str__(self):
		return self.category_name

class Tag(models.Model):
	tag_name = models.CharField(max_length=50)
	def __str__(self):
		return self.tag_name

class Article(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	create_time = models.DateTimeField('create_date', auto_now_add=True)
	update_time = models.DateTimeField('update_date', auto_now_add=True)
	category = models.ForeignKey(Category)
	tags = models.ManyToManyField(Tag)
	click_count = models.IntegerField(default=0)
	is_draft = models.BooleanField(default=True)
	def __str__(self):
		return self.title + ' ' + self.create_time.__str__()

class Comment(models.Model):
	content = models.TextField()
	parent = models.ForeignKey("self")
	article = models.ForeignKey(Article)
	user = models.ForeignKey(User)
	comment_time = models.DateTimeField()
	def __str__(self):
		return self.user.user_name + ' ' + self.comment_time.__str__()