from django.contrib import admin
from .models import *
from pagedown.widgets import AdminPagedownWidget
from django import forms

class UserAdmin(admin.ModelAdmin):
	fields = ['user_name', 'user_password', 'user_phone', 'user_email', 'create_date', 'update_date']
	search_fields = ['user_name']

class CategoryAdmin(admin.ModelAdmin):
	fields = ['category_name']
	search_fields = ['category_name']

class TagAdmin(admin.ModelAdmin):
	fields = ['tag_name']
	search_fields = ['tag_name']

class ArticleForm(forms.ModelForm):
	content = forms.CharField(widget=AdminPagedownWidget())

	class Meta:
		model = Article
		fields = '__all__'

class ArticleAdmin(admin.ModelAdmin):
	form = ArticleForm

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)