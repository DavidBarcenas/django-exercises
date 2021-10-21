from django.shortcuts import get_object_or_404, redirect, render

from comments.models import Comment
from comments.forms import CommentForm


def index(req):
    comments = Comment.objects.all()
    return render(req, 'index.html', {'comments': comments})


def add(req):
    if req.method == 'POST':
        form = CommentForm(req.POST)

        if form.is_valid():
            form.save()
            return redirect('comments:index')
    else:
        form = CommentForm()

    return render(req, 'add.html', {'form': form})


def update(req, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if req.method == 'POST':
        form = CommentForm(req.POST, instance=comment)

        if form.is_valid():
            form.save()
            return redirect('comments:update', pk=pk)
    else:
        form = CommentForm(instance=comment)

    return render(req, 'update.html', {
        'form': form,
        'comment': comment
    })
