from main.models import Tag, Artist, UserArtist, UserTagArtist

path = "hetrec2011-lastfm-2k"

def populate_database():
    delete_tables()
    tags = populate_tags()
    artists = populate_artists()
    populate_user_artists(artists)
    populate_user_tag_artists(tags, artists)
    print('Finished database population')

def delete_tables():  
    Tag.objects.all().delete()
    Artist.objects.all().delete()
    UserArtist.objects.all().delete()
    UserTagArtist.objects.all().delete()

def populate_tags():
    print('Populating tags...')
    tags = {}
    file = open(path + '/tags.dat', 'r', encoding='latin-1')
    for line in file.readlines()[1:-1]:
        line = line.strip().split('\t')
        tag_id = int(line[0])
        tags[tag_id] = Tag(id=tag_id, value=line[1])
    file.close()
    Tag.objects.bulk_create(tags.values())
    print(str(len(tags)) + ' tags inserted')
    return tags

def populate_artists():
    print('Populating artists...')
    artists = {}
    file = open(path + '/artists.dat', 'r', encoding='latin-1')
    for line in file.readlines()[1:-1]:
        line = line.strip().split('\t')
        artist_id = int(line[0])
        if len(line) == 4:
            picture_url = line[3]
        else:
            picture_url = ''
        artists[artist_id] = Artist(
            id=artist_id,
            name=line[1],
            url=line[2],
            picture_url=picture_url
        )
    file.close()
    Artist.objects.bulk_create(artists.values())
    print(str(len(artists)) + ' artists inserted')
    return artists

def populate_user_artists(artists):
    print('Populating user_artists...')
    elements = []
    file = open(path + '/user_artists.dat', 'r', encoding='latin-1')
    for line in file.readlines()[1:-1]:
        line = line.strip().split('\t')
        artist_id = int(line[1])
        if artist_id in artists:
            elements.append(UserArtist(
                user=int(line[0]),
                artist=artists[artist_id],
                listen_time=line[2]
            ))
    file.close()
    print(str(len(elements)) + ' user_artists inserted.')
    UserArtist.objects.bulk_create(elements)

def populate_user_tag_artists(tags, artists):
    print('Populating user_tag_artists...')
    elements = []
    file = open(path + '/user_taggedartists.dat', 'r', encoding='latin-1')
    for line in file.readlines()[1:-1]:
        line = line.strip().split('\t')
        artist_id = int(line[1])
        tag_id = int(line[2])
        if artist_id in artists and tag_id in tags:
            elements.append(UserTagArtist(
                user=int(line[0]),
                artist=artists[artist_id],
                tag=tags[tag_id],
                day=line[3],
                month=line[4],
                year=line[5]
            ))
    file.close()
    print(str(len(elements)) + ' user_tag_artists inserted.')
    UserTagArtist.objects.bulk_create(elements)