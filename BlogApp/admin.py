from django.contrib import admin
from BlogApp.models import Category,Blog,Comment





class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','category','author','status','is_featured')
    prepopulated_fields=  {'slug':('title',)}
    search_fields= ('category__category_name','status')
    list_editable= ('is_featured','status')

admin.site.register(Category)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Comment)
