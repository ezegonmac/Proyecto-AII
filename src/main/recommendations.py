#encoding:utf-8
from main.models import Artist, UserTagArtist, UserArtist
from collections import Counter
import shelve
from django.db.models import Count

def load_similarities():
    shelf = shelve.open('dataRS.dat')
    artist_tags = top_artist_tags()
    user_tags = top_users_tags(artist_tags)
    shelf['similarities'] = compute_similarities(artist_tags, user_tags)
    shelf.close()

def recommend_artists(user):
    res = []
    arts = UserArtist.objects.filter(user=user)
    if arts: # si existe el usuario
        shelf = shelve.open("dataRS.dat")
        #conjunto de artistas que ya ha escuchado el usuario, que no se consideran para recomendar
        listened = set()
        listened = set(a.artist.id for a in arts)
        for artist_id, score in shelf['similarities'][user]:
            if artist_id not in listened:
                artist_name = Artist.objects.get(pk=artist_id).name
                res.append([artist_name, 100 * score])
        shelf.close()
    return res

def compute_similarities(artist_tags, user_tags):
    # Calcula la matriz de similaridad entre usuarios y artistas (coeficiente de Dice). Sólo los 20 más similares se almacenan
    res = {}
    for u in user_tags:
        top_artists = {}
        for a in artist_tags:
            top_artists[a] = dice_coefficient(user_tags[u], artist_tags[a])
        res[u] = Counter(top_artists).most_common(20)
    return res

def top_artist_tags():
    # Calcula el conjunto de diez etiquetas más frecuentes de cada artista
    artists = {}
    anterior = -1
    suma = 1
    for e in UserTagArtist.objects.values('artist','tag').annotate(tag_count=Count('tag')).order_by('artist','-tag_count'):
        if e['artist'] == anterior and suma <= 10:
            artists[e['artist']].add(e['tag'])
            suma = suma + 1
        else:
            artists[e['artist']] = set([e['tag']])
            suma = 1
            anterior = e['artist']
    return artists
    

def top_users_tags(artists_tags):
    # Calcula el conjunto de etiquetas de los cinco artistas más escuchados por cada usuario
    users = {}
    anterior = -1
    suma = 1
    for e in UserArtist.objects.values('user','artist','listen_time').order_by('user','-listen_time'):
        if e['user'] == anterior and suma <= 5:
            if e['artist'] in artists_tags.keys():
                users[e['user']].union(artists_tags[e['artist']])
                suma = suma + 1
        else:
            if e['artist'] in artists_tags.keys():
                users[e['user']] = set(artists_tags[e['artist']])
                suma = 1
                anterior = e['user']
    return users


def dice_coefficient(set1, set2):
    return 2 * len(set1.intersection(set2)) / (len(set1) + len(set2))