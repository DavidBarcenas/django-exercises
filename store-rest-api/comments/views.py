from django.shortcuts import redirect, render

from comments.models import Comment
from comments.forms import CommentForm


def index(req):
    comments = Comment.objects.all()
    return render(req, 'index.html', {'comments': comments})


def add(req):

    if(req.method == 'POST'):
        form = CommentForm(req.POST)

        if form.is_valid():
            form.save()
            return redirect('comments:index')
    else:
        form = CommentForm()

    form = CommentForm
    return render(req, 'add.html', {'form': form})
