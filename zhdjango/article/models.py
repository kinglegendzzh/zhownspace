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


class Album(models.Model):
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cover_image = models.BigIntegerField(null=True, blank=True)  # 用于存储封面图片的文件ID
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    file_id = models.BigIntegerField(null=True, blank=True)  # 用于存储音频文件的文件ID
    def __str__(self):
        return self.name


class AudioFile(models.Model):
    filename = models.CharField(max_length=255)  # 文件名
    file_path = models.TextField()  # 文件在服务器上的路径
    file_md5 = models.CharField(max_length=32)  # 文件的MD5哈希值
    created_at = models.DateTimeField(auto_now_add=True)  # 文件上传的时间戳

    def __str__(self):
        return self.filename

    class Meta:
        db_table = 'audio_files'  # 指定表名为audio_files
