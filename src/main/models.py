from django.db import models
from django.core.validators import URLValidator
from django.contrib.auth.models import User


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.IntegerField()

    def __str__(self):
        return str(self.user) + ': ' + str(self.item)

    def get_user_liked_items_id(user):
        likes = Like.objects.filter(user=user)
        return [like.item for like in likes]

    def is_liked(user, item):
        return Like.objects.filter(user=user, item=item).exists()

    def get_items_id_liked_by_user(user):
        likes = Like.objects.filter(user=user)
        return [like.item for like in likes]
