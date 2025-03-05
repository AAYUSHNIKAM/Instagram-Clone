from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import Comment
from .models import Post, Message

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio', 'website'] 

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Add a comment...'}),
        }



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'hashtags']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']