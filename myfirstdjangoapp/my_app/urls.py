from django.urls import path
from . import views


app_name = 'my_app'

urlpatterns = [
    # Home
    # path('', views.home, name='home'),
    path('', views.Home.as_view(), name='home'),


    # Artist URLs
    path('artists/', views.artist_index, name='artist_index'),
    path('artists/<int:pk>/', views.artist_detail, name='artist_detail'),
    path('artists/create/', views.artist_create, name='artist_create'),
    path('artists/<int:pk>/update/', views.artist_update, name='artist_update'),
    path('artists/<int:pk>/delete/', views.artist_delete, name='artist_delete'),

    # Album URLs
    path('albums/', views.album_index, name='album_index'),
    path('albums/<int:pk>/', views.album_detail, name='album_detail'),
    path('albums/create/', views.album_create, name='album_create'),
    path('albums/<int:pk>/update/', views.album_update, name='album_update'),
    path('albums/<int:pk>/delete/', views.album_delete, name='album_delete'),

    # Song URLs
    path('songs/', views.song_index, name='song_index'),
    path('songs/<int:pk>/', views.song_detail, name='song_detail'),
    path('songs/create/', views.song_create, name='song_create'),
    path('songs/<int:pk>/update/', views.song_update, name='song_update'),
    path('songs/<int:pk>/delete/', views.song_delete, name='song_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login', views.signup, name='login'),

]

