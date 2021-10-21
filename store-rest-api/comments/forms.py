from django import forms
from django.forms import ModelForm, Textarea

from comments.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={'class': 'form-input'})
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=15, min_length=3)
    lastname = forms.CharField(required=False, max_length=15, min_length=3)
    phone = forms.RegexField(
        regex='\(\w{3}\)\w{3}-\w{4}',
        max_length=13,
        min_length=13
    )
    birth_date = forms.DateField()
