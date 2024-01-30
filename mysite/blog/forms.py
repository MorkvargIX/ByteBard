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

    def clean_tags(self):
        tags = self.cleaned_data['tags']

        min_length = 3
        max_length = 20

        for tag in tags:
            if len(tag) < min_length:
                self.add_error('tags', forms.ValidationError(f"All tags must be at least {min_length} characters long"))
            if len(tag) > max_length:
                self.add_error('tags', forms.ValidationError(f"All tags must be at most {max_length} characters long"))

        return tags


class SearchFrom(forms.Form):
    query = forms.CharField()


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    pass
