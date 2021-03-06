from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.base import ObjectDoesNotExist
from django.db.models.signals import post_save


class Post(models.Model):

    STATUS_CHOISES = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
    )

    title = models.CharField(max_length=30)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    slug = models.SlugField(max_length=250, unique=True)
    thumb = models.ImageField(upload_to='post_image', blank=True, default='default.png')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"post_pk": self.pk})

    def get_like_url(self):
        return reverse("blog:like-toggle", kwargs={"slug": self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length = 500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))

    def get_absolute_url(self):
        return reverse("poll:poll", kwargs={"poll_pk": self.pk})


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.pk})


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    bio = models.TextField(default='')
    #favorites = models.ManyToManyField(Post, related_name='favorited_by')

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_fav_url(self):
        return reverse("blog:fav-toggle", kwargs={"slug": self.slug})




