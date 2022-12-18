from django.db import models
from django.core.validators import URLValidator

class Tag(models.Model):
    value = models.CharField(max_length=20)

    def __str__(self):
        return self.value

class Artist(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(validators=[URLValidator()])
    picture_url = models.URLField(validators=[URLValidator()])
    
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class UserArtist(models.Model):
    user = models.IntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    listen_time = models.IntegerField()

    def _str__(self):
        return self.listen_time

class UserTagArtist(models.Model):
    user = models.IntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    day = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.day + '/' + self.month + '/' + self.year