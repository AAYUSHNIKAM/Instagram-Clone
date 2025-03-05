
from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

User = get_user_model()
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    caption = models.TextField()
    hashtags = models.CharField(max_length=255, blank=True, null=True)  # Allow empty hashtags
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user.username} - {self.caption[:20]}"


    def __str__(self):
        return f"{self.user.username} - {self.caption[:20]}"
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)  # Follow system
    following = models.ManyToManyField(User, related_name="followers", blank=True)  # Following system

    def __str__(self):
        return self.user.username


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text}"





class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_relations')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_relations')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    




# Reel Model
class Reel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reels")
    video = models.FileField(upload_to="reels/")
    caption = models.TextField(blank=True, null=True)
    hashtags = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_reels", blank=True)  # This field handles likes

    def total_likes(self):
        return self.likes.count()  # ✅ Use `likes.count()` instead of `reel_likes.count()`

    def total_comments(self):
        return self.comments.count()  # ✅ Use `comments.count()` instead of `reel_comments.count()`



# Reel Like
class ReelLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name="reel_likes")

# Reel Comment
class ReelComment(models.Model):
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on Reel {self.reel.id}"
    


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.message[:20]}"






CustomUser = get_user_model()
class Story(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stories")
    media = models.FileField(upload_to='stories/')  # Supports both images and videos
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        """Check if the story is older than 24 hours."""
        return timezone.now() - self.created_at > timezone.timedelta(hours=24)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"