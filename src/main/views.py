from collections import Counter

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from main.index import load_data
from main.index_details_search import get_all_details_names_by_id
from main.index_search import (search_all_by_ids_index, search_all_index,
                               search_by_id_index, search_items_index)
from main.models import Like, User
from main.recommendations import recommend_items
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

    # search and filtering default values
    default_search = ""
    default_brand, default_type, default_magnets = 'Any', 'Any', 'Any'

    default_page = 1

    active_search = default_search
    active_brand, active_type, active_magnets = default_brand, default_type, default_magnets

    active_page = default_page

    # like and filter actions
    if request.method == 'POST':
        if 'like' in request.POST:
            like(request)
            return HttpResponseRedirect(request.path_info)
        elif 'filter' in request.POST:
            active_search = request.POST.get('Search', default_search)
            active_brand = request.POST.get('Brand', default_brand)
            active_type = request.POST.get('Type', default_type)
            active_magnets = request.POST.get('Magnets', default_magnets)

            active_page = request.POST.get('Type', default_page)

    # url parameters
    if request.method == 'GET':
        active_search = request.GET.get('search', default_search)
        active_brand = request.GET.get('brand', default_brand)
        active_type = request.GET.get('type', default_type)
        active_magnets = request.GET.get('magnets', default_magnets)

        active_page = request.GET.get('page', default_page)

    # cast to int
    active_brand = int(active_brand) if active_brand.isnumeric() else default_brand
    active_type = int(active_type) if active_type.isnumeric() else default_type
    active_magnets = int(active_magnets) if active_magnets.isnumeric() else default_magnets

    [items, page, num_items] = search_items_index(
        active_brand, active_type, active_magnets, active_search, active_page, page_size=10
        )

    # choices for filters
    choices = get_all_details_names_by_id()

    likes = Like.get_user_liked_items_id(request.user)
    params = {
        'num_items': num_items,
        'items': items,
        'page': page,
        'likes': likes,
        'active_brand': active_brand,
        'active_type': active_type,
        'active_magnets': active_magnets,
        'search': active_search,
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

    user_id = request.user.id
    user = User.objects.get(id=user_id)
    liked_items_id = Like.get_user_liked_items_id(user)
    liked_items = search_all_by_ids_index(liked_items_id)
    params = {'liked_items': liked_items, 'likes': liked_items_id}

    return render(request, 'profile.html', params)


@require_http_methods(["GET"])
@login_required
def recommendations(request):
    user_id = request.user.id

    likes = Like.get_user_liked_items_id(request.user)
    recommended_items = recommend_items(user_id)[0:10]
    params = {
        'items': recommended_items,
        'num_items': len(recommended_items),
        'likes': likes,
        }

    return render(request, 'recommendations.html', params)


@require_http_methods(["GET", "POST"])
def signup(request):
    errors = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            errors = form.errors.values()
            errors = [item for sublist in errors for item in sublist]
    else:
        form = UserCreationForm()

    params = {'form': form, 'errors': errors}
    return render(request, 'registration/signup.html', params)
