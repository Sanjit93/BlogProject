"""BlogProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from BlogApp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('category/<int:category_id>/',views.posts_by_category, name='post_by_category'),
    path('blogs/<slug:slug>/',views.blogs, name='blogs'),
    path('Blogs/search/', views.search, name='search'),
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('Dashboard/categories/',views.categories,name='categories'),
    path('categories/add/',views.add_category, name='add_category'),
    path('Dashboard/categories/edit/<int:pk>/',views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/',views.delete_category, name='delete_category'),
    path('dashboard/posts/',views.posts, name='posts'),
    path('posts/add/',views.add_posts, name='addposts'),
    path('dashboard/posts/edit/<int:pk>/',views.edit_posts, name='editposts'),
    path('posts/delete/<int:pk>/',views.delete_posts, name='deleteposts'),
    path('dashboard/users/',views.users, name='users'),
    path('dashboard/users/add/',views.add_user, name='add_user'),
    path('users/edituser/<int:pk>/',views.edit_user, name='edituser'),
    path('users/delete/<int:pk>/',views.delete_user, name='deleteuser'),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
