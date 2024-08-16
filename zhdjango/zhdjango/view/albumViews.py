# views/album_views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from article.models import Album
from django.core.files.storage import FileSystemStorage
import os


@csrf_exempt
def create_album(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        artist = request.POST.get('artist')
        description = request.POST.get('description')
        cover_image = request.FILES.get('cover_image')

        if not all([name, artist, cover_image]):
            return JsonResponse({'error': 'Name, artist, and cover image are required'}, status=400)

        album = Album(name=name, artist=artist, description=description, cover_image=cover_image)
        album.save()

        return JsonResponse({'message': 'Album created successfully', 'album_id': album.id})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_album(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
        response = {
            'name': album.name,
            'artist': album.artist,
            'description': album.description,
            'cover_image': album.cover_image.url
        }
        return JsonResponse(response)
    except Album.DoesNotExist:
        return JsonResponse({'error': 'Album not found'}, status=404)


@csrf_exempt
def update_album(request, album_id):
    if request.method == 'POST':
        try:
            album = Album.objects.get(id=album_id)
            album.name = request.POST.get('name', album.name)
            album.artist = request.POST.get('artist', album.artist)
            album.description = request.POST.get('description', album.description)

            if 'cover_image' in request.FILES:
                album.cover_image = request.FILES['cover_image']

            album.save()

            return JsonResponse({'message': 'Album updated successfully'})
        except Album.DoesNotExist:
            return JsonResponse({'error': 'Album not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_album(request, album_id):
    if request.method == 'DELETE':
        try:
            album = Album.objects.get(id=album_id)
            album.delete()
            return JsonResponse({'message': 'Album deleted successfully'})
        except Album.DoesNotExist:
            return JsonResponse({'error': 'Album not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def list_albums(request):
    albums = Album.objects.all().values('id', 'name', 'artist', 'description', 'cover_image')
    albums_list = list(albums)
    return JsonResponse(albums_list, safe=False)
