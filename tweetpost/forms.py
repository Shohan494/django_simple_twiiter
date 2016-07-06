from django import forms
from .models import Tweet

# a custom form for tweet a post
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = (
            'content',
        )

    content = forms.CharField(
        max_length=140,
        widget=forms.Textarea(attrs={
            'placeholder': 'Tweet it out',
            'class': 'form-control',
            'rows': '3'
        })
    )
