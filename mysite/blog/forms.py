from django import forms
from django.contrib.auth.forms import BaseUserCreationForm, AuthenticationForm
from .models import Comment, Post


class SubscriptionForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'subscription-email-field', 'placeholder': 'Write your email for subscription'}),
        label=''
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body',]
        widgets = {
            'body': forms.Textarea(attrs={'class': 'rounded comment-form comment-form-input', 'name': 'body', 'placeholder': 'Write comment'}),
        }


class CreationPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write post title'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write tags'}),
        }


class SearchFrom(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'search',
            'class': 'form-control rounded',
            'style': 'your-title-style',
            'placeholder': 'Search....',
            'aria-label': "Search"
        }
    ))


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    pass
