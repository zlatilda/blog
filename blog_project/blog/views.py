from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, RedirectView
from django.utils import timezone
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
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
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            #user = form.save()
            form.save()
            profile = profile_form.save(commit=False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            profile.user = user
            profile.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('blog:index')
    else:
        form = RegForm()
        profile_form = ProfileForm()
    return render(request, 'registration/register.html', {'form': form, 'profile_form': profile_form})


"""def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.user = request.user
            form.save()

            return redirect('blog:index')
    else:
        form = ProfileForm()
    return render(request, 'registration/register.html', {'form': form})"""


def post_detail(request, post_pk):

    template = 'post_detail.html'
    post = get_object_or_404(Post, pk=post_pk)
    rand_post = Post.objects.order_by('?')

    fav = 1
    user = request.user
    if user.is_authenticated:
        if not Favorite.objects.filter(user=request.user, post=post):
            fav = 2
        else:
            fav = 3

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
        'favorite': fav,
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
    alph = Post.objects.all().order_by('title')

    if variable == 'date':
        context = {'items': older}

    if variable == 'likes':
        context = {'items': likes}

    if variable == 'alph':
        context = {'items': alph}

    return render(request, template, context)



def get_user_profile(request, pk):
    template = 'user_page.html'
    #user = User.objects.get(username=username)
    user = get_object_or_404(User, pk=pk)
    comments = Comment.objects.filter(user = user).order_by('-timestamp')

    items = Post.objects.all().filter(user=user).order_by('-created')
    favorites = Favorite.objects.filter(user=user)

    profile = UserProfile.objects.get(user=user)
    context = {
        'user': user,
        'comments': comments,
        'profile': profile,
        'items': items,
        'favorites':favorites,
    }
    return render(request, template, context)


def get_user_favourites(request, pk):
    template = 'list.html'
    user = get_object_or_404(User, pk=pk)
    favorites = Favorite.objects.filter(user=user)
    fav = []
    for obj in favorites:
        fav.append(obj.post)

    context = {'items': fav,}
    return render(request, template, context)


def user_settings(request):

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('blog:get_user_profile', request.user)
        else:
            return redirect('user-settings')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form, }
        return render(request, 'settings.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('blog:get_user_profile', request.user)
        else:
            return redirect('blog:change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'change_password.html', args)


class AddToFavorite(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        print(pk)
        obj = get_object_or_404(Post,pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            Favorite.objects.create(user=user, post=obj)
        return url_


class RemoveFromFavorite(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        print(pk)
        obj = get_object_or_404(Post,pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        fav = get_object_or_404(Favorite, post=obj, user=user)
        if user.is_authenticated:
            fav.delete()
        return url_


"""class PostFavouriteToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        print(slug)
        obj = get_object_or_404(UserProfile, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.favorites.all():
                obj.favorites.remove(user)
            else:
                obj.favorites.add(user)
        return url_"""


