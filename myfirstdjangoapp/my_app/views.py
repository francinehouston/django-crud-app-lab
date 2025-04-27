from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Song, Album, Artist
from .forms import SongForm, AlbumForm, ArtistForm
from datetime import date, timedelta


def home(request):
    return render(request, 'home.html')

# Song Views
def song_index(request):
    songs = Song.objects.all()
    return render(request, 'songs/song_index.html', {'songs': songs})

def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    return render(request, 'songs/song_detail.html', {'song': song})

# CREATE
def song_create(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            # Get duration values
            minutes = form.cleaned_data.get('duration_minutes')
            seconds = form.cleaned_data.get('duration_seconds')
            
            if minutes is None or seconds is None:
                form.add_error(None, "Duration minutes and seconds are required.")
                return render(request, 'songs/song_form.html', {'form': form, 'action': 'Create'})
            
            # Create timedelta for duration
            duration = timedelta(minutes=minutes, seconds=seconds)
            
            # Check if a new artist name was provided
            new_artist_name = form.cleaned_data.get('new_artist_name')
            if new_artist_name:
                # Create a new artist
                artist = Artist.objects.create(
                    name=new_artist_name,
                    genre='Unknown',  # Default genre
                    bio=''  # Empty bio
                )
                # Update the form's artist field with the new artist
                form.instance.artist = artist
            
            # Check if a new album name was provided
            new_album_name = form.cleaned_data.get('new_album_name')
            if new_album_name:
                # Create a new album
                album = Album.objects.create(
                    title=new_album_name,
                    artist=form.instance.artist or Artist.objects.first(),
                    release_date=date.today()
                )
                # Update the form's album field with the new album
                form.instance.album = album
            
            # Set the duration before saving
            form.instance.duration = duration
            
            song = form.save()
            messages.success(request, f'Song "{song.title}" created successfully!')
            return redirect('my_app:song_detail', pk=song.pk)
    else:
        form = SongForm()
    return render(request, 'songs/song_form.html', {'form': form, 'action': 'Create'})

# UPDATE
def song_update(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            song = form.save()
            messages.success(request, f'Song "{song.title}" updated successfully!')
            return redirect('my_app:song_detail', pk=song.pk)
    else:
        form = SongForm(instance=song)
        # Initialize duration fields
        total_seconds = song.duration.total_seconds()
        form.initial['duration_minutes'] = int(total_seconds // 60)
        form.initial['duration_seconds'] = int(total_seconds % 60)
    return render(request, 'songs/song_form.html', {'form': form, 'action': 'Update'})


def upload_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save()
            messages.success(request, f'Song "{song.title}" uploaded successfully!')
            return redirect('song_detail', pk=song.pk)
    else:
        form = SongForm()
    return render(request, 'songs/upload_song.html', {'form': form})

def song_list(request):
    songs = Song.objects.all()
    return render(request, 'song_list.html', {'songs': songs})

# DELETE
def song_delete(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        song.delete()
        messages.success(request, f'Song "{song.title}" deleted successfully!')
        return redirect('my_app:song_index')
    return render(request, 'songs/song_confirm_delete.html', {'song': song})

# Artist Views
def artist_index(request):
    artists = Artist.objects.all()
    return render(request, 'artists/artist_index.html', {'artists': artists})

def artist_detail(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    return render(request, 'artists/artist_detail.html', {'artist': artist})

def artist_create(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            artist = form.save()
            messages.success(request, f'Artist "{artist.name}" created successfully!')
            return redirect('my_app:artist_detail', pk=artist.pk)
    else:
        form = ArtistForm()
    return render(request, 'artists/artist_form.html', {'form': form, 'action': 'Create'})

def artist_update(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == 'POST':
        form = ArtistForm(request.POST, instance=artist)
        if form.is_valid():
            artist = form.save()
            messages.success(request, f'Artist "{artist.name}" updated successfully!')
            return redirect('my_app:artist_detail', pk=artist.pk)
    else:
        form = ArtistForm(instance=artist)
    return render(request, 'artists/artist_form.html', {'form': form, 'action': 'Update'})

def artist_delete(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == 'POST':
        artist.delete()
        messages.success(request, f'Artist "{artist.name}" deleted successfully!')
        return redirect('my_app:artist_index')
    return render(request, 'artists/artist_confirm_delete.html', {'artist': artist})

# Album Views
def album_index(request):
    albums = Album.objects.all()
    return render(request, 'albums/album_index.html', {'albums': albums})

def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    return render(request, 'albums/album_detail.html', {'album': album})

def album_create(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the new artist name
            new_artist_name = form.cleaned_data.get('new_artist_name')
            
            # Create a new artist or get existing one
            artist, created = Artist.objects.get_or_create(
                name=new_artist_name,
                defaults={
                    'genre': 'Unknown',
                    'bio': ''
                }
            )
            
            # Create the album with the artist
            album = form.save(commit=False)
            album.artist = artist
            album.save()
            
            messages.success(request, f'Album "{album.title}" created successfully!')
            return redirect('my_app:album_detail', pk=album.pk)
    else:
        form = AlbumForm()
    return render(request, 'albums/album_form.html', {'form': form, 'action': 'Create'})

def album_update(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            album = form.save()
            messages.success(request, f'Album "{album.title}" updated successfully!')
            return redirect('my_app:album_detail', pk=album.pk)
    else:
        form = AlbumForm(instance=album)
    return render(request, 'albums/album_form.html', {'form': form, 'action': 'Update'})

def album_delete(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        album.delete()
        messages.success(request, f'Album "{album.title}" deleted successfully!')
        return redirect('my_app:album_index')
    return render(request, 'albums/album_confirm_delete.html', {'album': album})

def create_artist(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            artist = form.save()
            messages.success(request, f'Artist "{artist.name}" created successfully!')
            return redirect('artist_detail', pk=artist.pk)
    else:
        form = ArtistForm()
    return render(request, 'artists/artist_form.html', {'form': form})

def update_song(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            song = form.save()
            messages.success(request, f'Song "{song.title}" updated successfully!')
            return redirect('my_app:song_detail', pk=song.pk)
    else:
        form = SongForm(instance=song)
    return render(request, 'songs/song_form.html', {'form': form, 'action': 'Update'})

def update_album(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            album = form.save()
            messages.success(request, f'Album "{album.title}" updated successfully!')
            return redirect('my_app:album_detail', pk=album.pk)
    else:
        form = AlbumForm(instance=album)
    return render(request, 'albums/album_form.html', {'form': form, 'action': 'Update'})

def update_artist(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == 'POST':
        form = ArtistForm(request.POST, instance=artist)
        if form.is_valid():
            artist = form.save()
            messages.success(request, f'Artist "{artist.name}" updated successfully!')
            return redirect('my_app:artist_detail', pk=artist.pk)
    else:
        form = ArtistForm(instance=artist)
    return render(request, 'artists/artist_form.html', {'form': form, 'action': 'Update'})
