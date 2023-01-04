from main.models import Like
from django.contrib.auth.models import User


def like(request):
    print(request.POST)
    user = request.POST.get('user_id')
    item = request.POST.get('product_id')

    user = User.objects.get(id=user)
    liked = Like.objects.filter(user=user, item=item).exists()
    if liked:
        Like.objects.filter(user=user, item=item).delete()
    elif not liked:
        like = Like(user=user, item=item)
        like.save()
