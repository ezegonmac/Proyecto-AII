from django.contrib import admin
from main.models import Like
from main.models import Tag, Artist, UserArtist, UserTagArtist

admin.site.register(Like)

admin.site.register(Tag)
admin.site.register(Artist)
admin.site.register(UserArtist)
admin.site.register(UserTagArtist)
