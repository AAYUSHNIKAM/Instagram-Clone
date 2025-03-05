from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import like_post

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/<str:username>/', views.profile, name='profile'),  
    path('create_post/', views.create_post, name='create_post'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('follow/<str:username>/', views.follow_unfollow, name='follow_unfollow'),
    path('reels/', views.reels_feed, name='reels_feed'),  
    path('create_reel/', views.create_reel, name='create_reel'),
    path('reel/<int:reel_id>/like/', views.like_reel, name='like_reel'),
    path("reel/<int:reel_id>/comment/", views.add_reel_comment, name="add_reel_comment"),
    path('reel/<int:reel_id>/delete/', views.delete_reel, name='delete_reel'),
    path("comment/<int:comment_id>/delete/", views.delete_reel_comment, name="delete_reel_comment"),
    path('chatbox/', views.chatbox, name='chatbox'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('upload_story/', views.upload_story, name='upload_story'),
    path('story/<int:story_id>/', views.view_story, name='view_story'),
    path('story/<int:story_id>/delete/', views.delete_story, name='delete_story'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
