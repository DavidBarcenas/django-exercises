from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.template import loader
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils.translation import gettext as _
import csv

from comments.models import Comment, Contact
from comments.forms import CommentForm, ContactForm, DivErrorList


def index(req):
    comments = Comment.objects.all()
    p = Paginator(comments, 5)

    page_number = req.GET.get('page')
    comments_page = p.get_page(page_number)

    return render(req, 'index_page.html', {'comments_page': comments_page})


def add(req):
    if req.method == 'POST':
        form = CommentForm(req.POST)

        if form.is_valid():
            comment = form.save()

            html_message = loader.render_to_string(
                'email/comment.html',
                {'comment', comment}
            )

            req.session['comment_id'] = comment.id

            send_mail(
                "Comment #" + str(comment.id),
                comment.text,
                "davee@gmail.com",
                ["juan@gmail.com"],
                fail_silently=False,
                html_message=html_message
            )

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


def contact(req):
    if req.method == 'POST':
        form = ContactForm(req.POST, req.FILES, error_class=DivErrorList)

        if form.is_valid():
            contact = Contact()

            if 'document' in req.FILES['document']:
                contact.document = req.FILES['document']

            contact.name = form.cleaned_data['name']
            contact.lastname = form.cleaned_data['lastname']
            contact.email = form.cleaned_data['email']
            contact.phone = form.cleaned_data['phone']
            contact.dirthdate = form.cleaned_data['dirthdate']

            contact.save()
    else:
        form = ContactForm()

    return render(req, 'contact.html', {'form': form})


def export(req):
    comments = Comment.objects.all()

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="comments.csv"'},
    )

    writer = csv.writer(response)

    for c in comments:
        writer.writerow([c.id, c.text])

    return response
