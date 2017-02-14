from django.db import models


# Create your models here.

class Phim(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    url_sha1 = models.CharField(max_length=40)
    title = models.TextField()
    url = models.CharField(max_length=2083)
    image = models.CharField(max_length=2083)
    type = models.CharField(max_length=255)
    quality = models.CharField(max_length=100)
    year = models.CharField(max_length=10)
    category = models.TextField()
    tags = models.TextField()
    description = models.TextField()
    time = models.CharField(max_length=10)
    actor = models.TextField()
    imdb = models.CharField(max_length=40)
    view = models.CharField(max_length=10)
    country = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    crawl_at = models.DateTimeField()

    class Meta:
        db_table = 'films'
