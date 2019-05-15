from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, RedirectView
from django.utils import timezone
from django.core.mail import send_mail
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


def signup(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('blog:create_profile')
    else:
        form = RegForm()
    return render(request, 'registration/register.html', {'form': form})


def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(commit=False)
            """form.user = request.user
            form.save()"""

            return redirect('blog:index')
    else:
        form = ProfileForm()
    return render(request, 'registration/register.html', {'form': form})


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
        items = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(user__username__icontains=query))
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


def edit_post(request, pk):
    template='post-edit.html'
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form=PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect('blog:index')
    else:
        form=PostForm(instance=post)

    context={
        'form': form,
        'post': post,
    }
    return render(request, template, context)


def order_by_params(request, variable):
    template="list.html"

    older = Post.objects.all().order_by('-created').reverse()
    likes = Post.objects.all().annotate(like_count=Count('likes')).order_by('-like_count')

    if variable == 'date':
        context = {'items': older}
        return render(request, template, context)

    if variable == 'likes':
        context = {'items': likes}
        return render(request, template, context)


def get_user_profile(request, username):
    template = 'user_page.html'
    user = User.objects.get(username=username)
    comments = Comment.objects.filter(user = user).order_by('-timestamp')

    items = Post.objects.all().filter(user=user).order_by('-created')

    profile = UserProfile.objects.get(user=user)
    context = {
        'user': user,
        'comments': comments,
        'profile': profile,
        'items': items,
    }
    return render(request, template, context)



