from django.views.decorators.csrf import csrf_exempt
from article.models import Article, Comment
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

@csrf_exempt
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
        comments = Comment.objects.filter(article=article)
        data = {
            "title": article.title,
            "image": article.image.url if article.image else None,
            "content": article.content,
            "published_at": article.published_at,
            "modified_at": article.modified_at,
            "comments": [
                {"author": comment.author, "content": comment.content, "created_at": comment.created_at}
                for comment in comments
            ]
        }
        return JsonResponse(data)
    except Article.DoesNotExist:
        return JsonResponse({"error": "Article not found"}, status=404)


@csrf_exempt
def list_articles(request):
    # 获取所有文章，按照发布时间倒序排列
    articles = Article.objects.all().order_by('-published_at').values(
        'id', 'title', 'image', 'published_at'
    )
    # 构造响应
    return JsonResponse(list(articles), safe=False)



# 创建评论
@csrf_exempt
@require_http_methods(["POST"])
def create_comment(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        data = json.loads(request.body)
        comment = Comment.objects.create(
            article=article,
            author=data.get('author'),
            content=data.get('content')
        )
        return JsonResponse({
            "id": comment.id,
            "author": comment.author,
            "content": comment.content,
            "created_at": comment.created_at
        })
    except Article.DoesNotExist:
        return JsonResponse({"error": "Article not found"}, status=404)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

# 删除评论
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return JsonResponse({"message": "Comment deleted successfully"})
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Comment not found"}, status=404)

# 更新评论
@csrf_exempt
@require_http_methods(["PUT"])
def update_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        data = json.loads(request.body)
        comment.author = data.get('author', comment.author)
        comment.content = data.get('content', comment.content)
        comment.save()
        return JsonResponse({
            "id": comment.id,
            "author": comment.author,
            "content": comment.content,
            "created_at": comment.created_at
        })
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Comment not found"}, status=404)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

# 获取某篇文章的所有评论
@csrf_exempt
@require_http_methods(["GET"])
def get_comments(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        comments = Comment.objects.filter(article=article).values(
            "id", "author", "content", "created_at"
        )
        return JsonResponse(list(comments), safe=False)
    except Article.DoesNotExist:
        return JsonResponse({"error": "Article not found"}, status=404)

# 创建文章
@require_http_methods(["POST"])
@csrf_exempt
def create_article(request):
    try:
        data = json.loads(request.body)
        article = Article.objects.create(
            title=data.get('title'),
            image=data.get('image'),  # 假设前端传递图片的 URL 或路径
            content=data.get('content')
        )
        return JsonResponse({
            "id": article.id,
            "title": article.title,
            "image": article.image.url if article.image else None,
            "content": article.content,
            "published_at": article.published_at,
            "modified_at": article.modified_at
        })
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

# 删除文章
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        article.delete()
        return JsonResponse({"message": "Article deleted successfully"})
    except Article.DoesNotExist:
        return JsonResponse({"error": "Article not found"}, status=404)

# 更新文章
@csrf_exempt
@require_http_methods(["PUT"])
def update_article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        data = json.loads(request.body)
        article.title = data.get('title', article.title)
        article.image = data.get('image', article.image)
        article.content = data.get('content', article.content)
        article.save()
        return JsonResponse({
            "id": article.id,
            "title": article.title,
            "image": article.image.url if article.image else None,
            "content": article.content,
            "published_at": article.published_at,
            "modified_at": article.modified_at
        })
    except Article.DoesNotExist:
        return JsonResponse({"error": "Article not found"}, status=404)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

# 获取文章详情
@csrf_exempt
@require_http_methods(["GET"])
def get_article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        data = {
            "id": article.id,
            "title": article.title,
            "image": article.image.url if article.image else None,
            "content": article.content,
            "published_at": article.published_at,
            "modified_at": article.modified_at,
        }
        return JsonResponse(data)
    except Article.DoesNotExist:
        return JsonResponse({"error": "Article not found"}, status=404)
