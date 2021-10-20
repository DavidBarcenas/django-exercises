from django.shortcuts import render

from comments.models import Comment


def index(req):
    comments = Comment.objects.all()

    return render(req, 'index.html', {'comments': comments})
