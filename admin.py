from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
	fields = ['user_name', 'user_password', 'user_phone', 'user_email', 'create_date', 'update_date']
	search_fields = ['user_name']

class CategoryAdmin(admin.ModelAdmin):
	fields = ['category_name']
	search_fields = ['category_name']

class TagAdmin(admin.ModelAdmin):
	fields = ['tag_name']
	search_fields = ['tag_name']


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Article)
admin.site.register(Comment)