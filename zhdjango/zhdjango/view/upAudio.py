from django.http import HttpResponse

import os
import hashlib
import sqlite3
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# 设置文件保存路径
localPath = 'lib/'


# 创建 SQLite3 数据库连接的函数
def get_db_connection():
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    conn = sqlite3.connect(db_path)
    return conn


# 计算文件的 MD5 哈希值
def calculate_md5(file):
    hash_md5 = hashlib.md5()
    for chunk in file.chunks():
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


@csrf_exempt
def upAudio(request):
    if request.method == 'POST':
        file = request.FILES['file']
        fs = FileSystemStorage()

        # 计算文件的MD5值
        file_md5 = calculate_md5(file)

        # 打开数据库连接
        conn = get_db_connection()
        cursor = conn.cursor()

        # 检查数据库中是否存在相同名称或相同MD5的文件
        cursor.execute("SELECT id, filename, file_path, file_md5 FROM audio_files WHERE filename = ? OR file_md5 = ?",
                       (file.name, file_md5))
        existing_file = cursor.fetchone()

        if existing_file:
            # 如果文件已存在，返回文件信息
            file_id, filename, file_path, file_md5_db = existing_file
            conn.close()
            return JsonResponse({'file_id': file_id, 'file_url': file_path, 'message': 'File already exists'})

        # 如果文件不存在，保存文件并将信息存储到数据库
        filename = fs.save(localPath + file.name, file)
        file_path = fs.path(filename)

        # 将文件信息插入数据库
        cursor.execute('INSERT INTO audio_files (filename, file_path, file_md5) VALUES (?, ?, ?)',
                       (file.name, file_path, file_md5))
        conn.commit()

        # 获取文件ID
        file_id = cursor.lastrowid

        # 关闭数据库连接
        conn.close()

        return JsonResponse({'file_id': file_id, 'file_url': file_path, 'message': 'File uploaded successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def getAudioStream(request):
    if request.method == 'GET':
        file_id = request.GET.get('file_id', None)

        if not file_id:
            return JsonResponse({'error': 'file_id parameter is required'}, status=400)

        # 每个请求创建新的连接
        conn = get_db_connection()
        cursor = conn.cursor()

        # 从数据库中查询文件路径
        cursor.execute('SELECT file_path FROM audio_files WHERE id = ?', (file_id,))
        result = cursor.fetchone()

        # 关闭数据库连接
        conn.close()

        if not result:
            return JsonResponse({'error': 'File not found'}, status=404)

        file_path = result[0]

        # 读取文件并返回文件流
        try:
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='audio/mpeg')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
        except Exception as e:
            logging.error(f"Error reading file: {e}")
            return JsonResponse({'error': 'Failed to read the file'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
