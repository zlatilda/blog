from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
# Create your views here.


def index(request):
    template = 'list.html'
    items = Post.objects.all().order_by('-created')
    context = {

        'items': items,
    }
    return render(request, template, context)


def signup(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:create_profile')
    else:
        form = RegForm()
    return render(request, 'registration/register.html', {'form': form})


def create_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(data=request.POST, files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('blog:index')
    else:
        profile_form = ProfileForm()
    return render(request, 'registration/register.html', {'profile_form': profile_form})


def post_detail(request, post_pk):

    template = 'post_detail.html'
    post = get_object_or_404(Post, pk=post_pk)
    rand_post = Post.objects.order_by('?')

    #images = Images.objects.filter(slug=post.slug)

    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(post=post, user=request.user, content=content)
            comment.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'rand_post': rand_post[:5],
        'comments': comments,
        'comment_form': comment_form,
        #'images': images,
    }
    return render(request, template, context)





