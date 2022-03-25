from django import forms
from .models import ReviewComment, BookComment

class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        fields = ['text']
        widgets = {
            'body' : forms.Textarea(attrs={
                'rows': '5',
                'cols': '40',
                'maxlength': '600',
            }),
        }

class BookCommentForm(forms.ModelForm):
    class Meta:
        model = BookComment
        fields = ['text']
        widgets = {
            'body' : forms.Textarea(attrs={
                'rows': '5',
                'cols': '40',
                'maxlength': '600',
            }),
        }