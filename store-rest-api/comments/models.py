from django.db import models


class Comment(models.Model):
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return 'Comment #{}'.format(self.id)
