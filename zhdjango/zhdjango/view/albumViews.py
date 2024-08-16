from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from article.models import Album
from django.core.files.storage import FileSystemStorage
import os
import sqlite3
import json

from zhdjango import settings


def get_db_connection():
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    print(f"Connecting to database at {db_path}")  # 添加打印以检查路径
    conn = sqlite3.connect(db_path)
    return conn


@csrf_exempt
def create_album(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            artist = data.get('artist')
            description = data.get('description')
            cover_image_id = data.get('cover_image_id')
            file_id = data.get('file_id')

            if not all([name, artist, cover_image_id, file_id]):
                return JsonResponse({'error': 'Name, artist, cover image ID, and file ID are required'}, status=400)

            album = Album(
                name=name,
                artist=artist,
                description=description,
                cover_image=cover_image_id,
                file_id=file_id
            )
            album.save()

            return JsonResponse({'message': 'Album created successfully', 'album_id': album.id})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_album(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
        response = {
            'name': album.name,
            'artist': album.artist,
            'description': album.description,
            'cover_image_id': album.cover_image,
            'file_id': album.file_id
        }
        return JsonResponse(response)
    except Album.DoesNotExist:
        return JsonResponse({'error': 'Album not found'}, status=404)


@csrf_exempt
def update_album(request, album_id):
    if request.method == 'POST':
        try:
            album = Album.objects.get(id=album_id)
            data = json.loads(request.body)

            album.name = data.get('name', album.name)
            album.artist = data.get('artist', album.artist)
            album.description = data.get('description', album.description)
            album.cover_image = data.get('cover_image_id', album.cover_image)
            album.file_id = data.get('file_id', album.file_id)

            album.save()

            return JsonResponse({'message': 'Album updated successfully'})
        except Album.DoesNotExist:
            return JsonResponse({'error': 'Album not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
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
    albums = Album.objects.all().values('id', 'name', 'artist', 'description', 'cover_image', 'file_id')
    albums_list = list(albums)
    return JsonResponse(albums_list, safe=False)
