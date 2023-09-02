import graphene
from graphene_django import DjangoObjectType
from .models import Artist, Album, Song

# Define GraphQL types for the models
class ArtistType(DjangoObjectType):
    class Meta:
        model = Artist
        fields = ("id", "name")

class AlbumType(DjangoObjectType):
    class Meta:
        model = Album
        fields = ("id", "title", "artist", "release_date")

class SongType(DjangoObjectType):
    class Meta:
        model = Song
        fields = ("id", "title", "album", "audio_file")


class Query(graphene.ObjectType):
    all_artists = graphene.List(ArtistType)
    all_albums = graphene.List(AlbumType)
    all_songs = graphene.List(SongType)
        # get a single artist by ID
    artist = graphene.Field(ArtistType, id=graphene.ID(required=True))
     #  get a single album by ID
    album = graphene.Field(AlbumType, id=graphene.ID(required=True))
        # New query to get a single song by ID
    song = graphene.Field(SongType, id=graphene.ID(required=True))

    def resolve_song(root, info, id):
        return Song.objects.get(pk=id)
    
    def resolve_album(root, info, id):  
        return Album.objects.get(pk=id)
    
    def resolve_artist(root, info, id):
        return Artist.objects.get(pk=id)
    
    def resolve_all_artists(root, info):
        return Artist.objects.all()
    
    def resolve_all_albums(root, info):
        return Album.objects.all()

    def resolve_all_songs(root, info):
        return Song.objects.all()




class CreateArtist(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    artist = graphene.Field(ArtistType)

    def mutate(self, info, name):
        artist = Artist(name=name)
        artist.save()
        return CreateArtist(artist=artist)

class CreateAlbum(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        artist_id = graphene.ID(required=True)
        release_date = graphene.Date(required=True)

    album = graphene.Field(AlbumType)

    def mutate(self, info, title, artist_id, release_date):
        artist = Artist.objects.get(id=artist_id)
        album = Album(title=title, artist=artist, release_date=release_date)
        album.save()
        return CreateAlbum(album=album)

class CreateSong(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        album_id = graphene.ID(required=True)
        audio_file = graphene.String(required=True)

    song = graphene.Field(SongType)

    def mutate(self, info, title, album_id, audio_file):
        album = Album.objects.get(id=album_id)
        song = Song(title=title, album=album, audio_file=audio_file)
        song.save()
        return CreateSong(song=song)
class DeleteItem(graphene.Mutation):
    class Arguments:
        item_id = graphene.ID(required=True)
        item_type = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, item_id, item_type):
        try:
            if item_type == "artist":
                Artist.objects.get(pk=item_id).delete()
            elif item_type == "album":
                Album.objects.get(pk=item_id).delete()
            elif item_type == "song":
                Song.objects.get(pk=item_id).delete()
            else:
                raise Exception("Invalid item type")
            return DeleteItem(success=True)
        except Exception as e:
            return DeleteItem(success=False, error=str(e))
# Create the schema    

class Mutation(graphene.ObjectType):
    create_artist = CreateArtist.Field()
    create_album = CreateAlbum.Field()
    create_song = CreateSong.Field()
    delete_item = DeleteItem.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)