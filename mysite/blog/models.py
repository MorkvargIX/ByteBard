from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    doby = models.TextField()

    def __str__(self):
        return self.title

