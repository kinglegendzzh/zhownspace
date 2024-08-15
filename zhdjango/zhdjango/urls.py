"""zhdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .view.chordRecognitionView import ChordRecognitionView
from .view.detail import article_detail
from .view.upAudio import upAudio, getAudioStream
from .view.login import httpTest, jsonTest
from .view.detail import (
    create_article, delete_article, update_article, get_article,
    create_comment, delete_comment, update_comment, get_comments,
    list_articles,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('zhown/up/', upAudio, name='upload_audio_post'),
    path('zhown/get/', getAudioStream, name='upload_audio_get'),
    path('zhown/httpTest/', httpTest, name='httpTest'),
    path('zhown/jsonTest/', jsonTest, name='jsonTest'),
    path('zhown/chord/recognize/', ChordRecognitionView.as_view(), name='recognize-chord'),
    path('api/article/<int:pk>/', article_detail, name='article-detail'),
    path('api/article/', create_article, name='create-article'),
    path('api/article/<int:article_id>/', get_article, name='get-article'),
    path('api/article/<int:article_id>/update/', update_article, name='update-article'),
    path('api/article/<int:article_id>/delete/', delete_article, name='delete-article'),
    path('api/article/<int:article_id>/comments/', get_comments, name='get-comments'),
    path('api/article/<int:article_id>/comments/create/', create_comment, name='create-comment'),
    path('api/comment/<int:comment_id>/delete/', delete_comment, name='delete-comment'),
    path('api/comment/<int:comment_id>/update/', update_comment, name='update-comment'),
    path('api/articles/', list_articles, name='list-articles'),
]
