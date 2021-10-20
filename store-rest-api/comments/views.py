from django.shortcuts import render

from comments.models import Comment
from comments.forms import CommentForm


def index(req):
    comments = Comment.objects.all()
    return render(req, 'index.html', {'comments': comments})


def add(req):
    form = CommentForm
    return render(req, 'add.html', {'form': form})
