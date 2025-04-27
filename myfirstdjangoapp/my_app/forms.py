from django import forms
from .models import Song, Album, Artist
from datetime import timedelta

# class SongForm(forms.ModelForm):
#     class Meta:
#         model = Song
#         fields = ['title', 'album', 'duration', 'audio_file']
        
# class ArtistForm(forms.ModelForm):
#     class Meta: 
#         model = Artist
#         fields = ['name', 'bio']
        
# class AlbumForm(forms.ModelForm):
#     class Meta:
#         model = Album
#         fields = ['title', 'artist', 'release_date', 'cover_image']

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'genre', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class AlbumForm(forms.ModelForm):
    new_artist_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter artist name'}),
        label='Artist Name'
    )

    class Meta:
        model = Album
        fields = ['title', 'release_date', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class SongForm(forms.ModelForm):
    duration_minutes = forms.IntegerField(
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minutes'})
    )
    duration_seconds = forms.IntegerField(
        min_value=0,
        max_value=59,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Seconds'})
    )
    new_album_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter album name'}),
        label='Album Name'
    )
    new_artist_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new artist name'}),
        label='Or create new artist'
    )

    class Meta:
        model = Song
        fields = ['title', 'audio_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'audio_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'audio/*'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        minutes = cleaned_data.get('duration_minutes', 0)
        seconds = cleaned_data.get('duration_seconds', 0)
        
        if minutes is None or seconds is None:
            raise forms.ValidationError("Duration minutes and seconds are required.")
            
        cleaned_data['duration'] = timedelta(minutes=minutes, seconds=seconds)
        return cleaned_data