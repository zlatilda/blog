from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Comment, Post


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('thumb', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }


class RegForm(forms.ModelForm):

    username = forms.CharField(max_length=30, help_text="Enter your username (30 letter or less)."
                               , widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'id': 'username'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}))
    password1 = forms.CharField(max_length=32, label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}), )
    password2 = forms.CharField(max_length=32, label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'assert_password'}), )

    class Meta:
        model = User

        fields = ('username', 'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'style': 'resize:none; height: 5em;'})
        }


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'body', 'thumb',)
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

