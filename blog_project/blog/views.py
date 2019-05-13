from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, RedirectView
from django.utils import timezone
# Create your views here.


def index(request):
    template = 'list.html'
    items = Post.objects.all().order_by('-created')

    page = request.GET.get('page', 1)

    paginator = Paginator(items, 9)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

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
            return redirect('blog:index')
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


def search(request):

    template = "list.html"
    query = request.GET.get('q')
    if query:
        items = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
    else:
        items = Post.objects.all()
    content = {
        'items': items,
    }

    return render(request, template, content)


def comment_delete(request, pk):
    comment = Comment.objects.get(pk=pk)
    if comment.user == request.user:
        comment.is_removed = True
        comment.save()
        comment.delete()

    return redirect(request.META['HTTP_REFERER'])


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:index')


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        print(slug)
        obj = get_object_or_404(Post, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


def post_new(request):
    template = 'post-edit.html'

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.created = timezone.now()
            post.save()
        return redirect('blog:index')
    else:
        form = PostForm()

    content = {
        'form': form
    }
    return render(request, template, content)




