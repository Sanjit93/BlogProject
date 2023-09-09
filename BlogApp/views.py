from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from BlogApp.models import Category,Blog, Comment
from BlogProject.forms import AddUserForm, EditUserForm, RegistrationForm,CategoryForm,BlogPostForm
from socialmedApp.models import About
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User



# Create your views here.
def home(request):
    featured_posts = Blog.objects.filter(is_featured=True,status="Published").order_by('-updated_at')
    posts = Blog.objects.filter(is_featured=False,status="Published")
    try:
        about= About.objects.get()
    except:
        about= None
    context = {
        'featured_posts' : featured_posts,
        'posts':posts,
        'about':about,
        
    }
    return render(request, 'BlogApp/home.html', context)

def posts_by_category(request,category_id):
    
    posts=Blog.objects.filter(status='Published',category=category_id)
    #try:
    #    category = Category.objects.get(pk=category_id)
    #except:
    #    return redirect('home')
    category=get_object_or_404(Category, pk=category_id)
    context={
        'posts':posts,
        'category':category,
        
    }
    return render(request,'BlogApp/posts.html',context)

def blogs(request, slug):
    single_post=get_object_or_404(Blog,slug=slug,status='Published')
    if request.method=='POST':
        comment=Comment()
        comment.user=request.user
        comment.blog=single_post
        comment.comment=request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)
    # comment
    comment= Comment.objects.filter(blog=single_post)
    comment_count=comment.count()
    return render(request, 'BlogApp/blogs.html',{'single_post':single_post,'comment':comment,'comment_count':comment_count})

def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword),status='Published')
    return render(request,'BlogApp/search.html',{'blogs':blogs,'keyword':keyword})

def register(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'congratulation!! you have registered successfully')
            form.save()
            return redirect('register')
    else:
        form = RegistrationForm()
    return render(request, 'BlogApp/register.html',{'form': form})

def login(request):
    if request.method == 'POST':
        form=AuthenticationForm(request,request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
            return redirect('home')
    form=AuthenticationForm()
    contex={
        'form':form
    }
    return render(request, 'BlogApp/login.html',contex)

def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    category_count=Category.objects.all().count()
    blogs_count=Blog.objects.all().count()
    context={
        'category_count': category_count,
        'blogs_count': blogs_count,
    }
    return render(request,'dashboard/dashboard.html',context)

def categories(request):
    return render(request,'dashboard/category.html')

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')

    form = CategoryForm()
    context={
        'form':form,
    }
    return render(request,'dashboard/add_category.html',context)

def edit_category(request, pk):
    category = get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')

    form=CategoryForm(instance=category)
    context={
        'form':form,
        'category':category,
    }
    return render(request,'dashboard/edit.html',context)

def delete_category(request,pk):
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    return redirect('categories')
 
def posts(request):
    post=Blog.objects.all()
    return render(request, 'dashboard/postsby.html',{'post':post})

def add_posts(request):
     if request.method == 'POST':
        form = BlogPostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-'+str(post.id)
            post.save()
            return redirect('posts')

     form=BlogPostForm()
     context={
        'form':form,
        
       }
     form= BlogPostForm()
     return render(request,'dashboard/addposts.html',context)

def edit_posts(request,pk):
    post = get_object_or_404(Blog,pk=pk)
    if request.method == 'POST':
        form =BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-'+str(post.id)
            post.save()
            return redirect('posts')
    form =BlogPostForm(instance=post)
    return render(request, 'dashboard/editposts.html',{'form':form,'post':post})

def delete_posts(request,pk):
    post = get_object_or_404(Blog,pk=pk)
    post.delete()
    return redirect('posts')

def users(request):
    users = User.objects.all()
    return render(request, 'dashboard/user.html',{'users':users})

def add_user(request):
    if request.method=='POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    form= AddUserForm()
    return render(request,'dashboard/adduser.html',{'form':form})

def edit_user(request,pk):
    user= get_object_or_404(User,pk=pk)
    if request.method == 'POST':
             form = EditUserForm(request.POST, instance=user)
             if form.is_valid():
                   form.save()
                   return redirect('users')
    form= EditUserForm(instance=user)
    return render(request,'dashboard/edituser.html',{'form':form})

def delete_user(request,pk):
    user=get_object_or_404(User,pk=pk)
    user.delete()
    return redirect('users')