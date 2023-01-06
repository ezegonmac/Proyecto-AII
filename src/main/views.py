from collections import Counter

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, render
from django.views.decorators.http import require_http_methods

from main.forms import ArtistForm, UserForm
from main.index import load_data
from main.index_search import search_all_index, search_by_id_index, search_items_index
from main.index_details_search import get_all_details_names_by_id
from main.models import Like, UserArtist, UserTagArtist
from main.populate import populate_database
from main.recommendations import load_similarities, recommend_artists
from main.utils import like


@require_http_methods(["GET"])
def index(request):
    return render(request, 'index.html')


@require_http_methods(["GET"])
def home(request): 
    return render(request, 'home.html')


@require_http_methods(["GET"])
@permission_required('is_superuser')
def scraping(request):
    items = load_data()
    params = {'num_items': len(items), 'items': items}
    return render(request, 'scraping.html', params)


@require_http_methods(["GET"])
@permission_required('is_superuser')
def search_all(request):
    items = search_all_index()
    all_details_names_by_id = get_all_details_names_by_id()
    params = {'num_items': len(items), 'items': items, **all_details_names_by_id}
    return render(request, 'search_all.html', params)


@require_http_methods(["GET", "POST"])
@login_required
def catalog(request):

    search = ""
    brand, type = 'Any', 'Any'

    if request.method == 'POST':
        if 'like' in request.POST:
            like(request)
            return HttpResponseRedirect(request.path_info)
        elif 'filter' in request.POST:
            search = request.POST.get('Search', search)
            brand = request.POST.get('Brand', brand)
            type = request.POST.get('Type', type)

# TODO: poner como brand y type arriba ?¿
    if request.GET.get('search'):
        search = request.GET.get('search')
    if request.GET.get('brand'):
        brand = request.GET.get('brand')
    if request.GET.get('type'):
        type = request.GET.get('type')
    [items, page, num_items] = search_items_index(
        brand, type, search, request, page_size=10
        )

    # cast to int
    brand = int(brand) if brand != 'Any' else None
    type = int(type) if type != 'Any' else None

    choices = get_all_details_names_by_id()

    likes = Like.get_user_liked_items(request.user)
    params = {
        'num_items': num_items,
        'items': items,
        'page': page,
        'likes': likes,
        'active_brand': brand,
        'active_type': type,
        'search': search,
        **choices
        }

    return render(request, 'catalog.html', params)


@require_http_methods(["GET", "POST"])
@login_required
def product_detail(request, id):

    if request.method == 'POST' and 'like' in request.POST:
        like(request)

    item = search_by_id_index(id)
    liked = Like.is_liked(request.user, id)
    all_details_names_by_id = get_all_details_names_by_id()
    params = {'item': item, 'liked': liked, **all_details_names_by_id}
    return render(request, 'product_detail.html', params)


@require_http_methods(["GET"])
@login_required
def profile(request):
    return render(request, 'profile.html')


def populateDB(request):
    populate_database()
    return render(request, 'populate.html')

def loadRS(request):
    load_similarities()
    return render(request,'loadRS.html')

def mostListenedArtists(request):
    form = UserForm(request.GET, request.FILES)
    if form.is_valid():
        user = form.cleaned_data['id'] 
        user_artists = UserArtist.objects.filter(user=user).order_by('-listen_time')[:5]
        params = {'form': form, 'user_artists': user_artists}
    else:
        params = {'form': UserForm()}
    return render(request,'mostListenedArtists.html', params)

def mostFrequentTags(request):
    form = ArtistForm(request.GET, request.FILES)
    if form.is_valid():
        artist = form.cleaned_data['id']
        tags = [
            elem.tag.value
            for elem in get_list_or_404(UserTagArtist, artist=artist)
        ]
        params = {'form': form, 'tags': Counter(tags).most_common(10)}
    else:
        params = {'form': ArtistForm()}
    return render(request,'mostFrequentTags.html', params)

def recommendedArtists(request):
    form = UserForm(request.GET, request.FILES)
    if form.is_valid():
        user = form.cleaned_data['id']
        artists = recommend_artists(int(user))
        params = {'form': form, 'artists': artists}
    else:
        params = {'form': UserForm()}
    return render(request,'recommendedArtists.html', params)

def styles(request): 
    return render(request,'styles.html')