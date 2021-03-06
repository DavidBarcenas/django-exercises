from django import forms
from django.forms import ModelForm, Textarea
from django.core.validators import EmailValidator, MinLengthValidator
from django.forms.utils import ErrorList

from comments.models import Comment, TypeContact


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={'class': 'form-input'})
        }


class ContactForm(forms.Form):
    CHOICES = (
        (1, 'Bussiness'),
        (2, 'Personal'),
        (3, 'Other'),
    )

    name = forms.CharField(validators=[
        MinLengthValidator(2, message='Name Error %(limit_value)d')
    ])
    lastname = forms.CharField(required=False, max_length=15, min_length=3)
    phone = forms.RegexField(
        regex='\(\w{3}\)\w{3}-\w{4}',
        max_length=13,
        min_length=13
    )
    email = forms.EmailField(validators=[EmailValidator()])
    birth_date = forms.DateField()
    # contact = forms.ChoiceField(queryset=TypeContact.objects.all())
    document = forms.FileField(required=False)
    terms = forms.BooleanField()


class DivErrorList(ErrorList):
    def __str__(self):
        return ''

    def as_divs(self):
        if not self:
            return ''
        return ''
