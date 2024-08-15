from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
