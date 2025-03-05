from django.shortcuts import render, redirect
from .models import Follow, Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from .forms import ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.models import  User
from .forms import ProfileEditForm
from .models import Profile
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .models import Follow, Post, PostImage, Comment, Reel, Profile, ReelComment, ReelLike, Message, Story
from django.http import HttpResponseForbidden
from .forms import PostForm, CommentForm, ProfileEditForm, MessageForm
from django.http import JsonResponse
from django.contrib import messages
import json
from accounts.models import CustomUser
import time
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta




User = get_user_model()

@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')

    # Get stories from the logged-in user and the users they follow
    following_users = request.user.following_relations.all().values_list('following', flat=True)
    valid_users = list(following_users) + [request.user.id]  # Include the logged-in user's stories
    stories = Story.objects.filter(user__in=valid_users, created_at__gte=now() - timedelta(hours=24))

    print("Fetched stories:", stories)  # Debugging output

    return render(request, 'posts/home.html', {'posts': posts, 'stories': stories})






@login_required


# def profile(request, username):
#     user = get_object_or_404(User, username=username)
#     profile = user.profile

#     following_users = profile.following.all()
#     followers_users = profile.followers.all()

#     context = {
#         'user': user,
#         'profile': profile,
#         'posts': Post.objects.filter(user=user),
#         'following_users': following_users,
#         'followers_users': followers_users,
#     }

#     return render(request, 'posts/profile.html', context)





# def profile(request, username):
#     user = get_object_or_404(User, username=username)
    
    
#     # Fetch followers and following using Follow model
#     followers_users = User.objects.filter(follower_relations__following=user)
#     following_users = User.objects.filter(following_relations__follower=user)

#     context = {
#         'user': user,
#         'posts': Post.objects.filter(user=user),
#         'followers_users': followers_users,
#         'following_users': following_users,
#     }
    
#     return render(request, 'posts/profile.html', context)



# def profile(request, username):
#     user = get_object_or_404(User, username=username)
#     profile = user.profile

#     # Get the list of users this user is following
#     following_users = profile.user.following.all()  

#     context = {
#         'user': user,
#         'profile': profile,
#         'following_users': following_users,  # Pass this to the template
#     }
#     return render(request, 'posts/profile.html', context)


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

    # Fetch followers and following using Follow model
    followers_users = User.objects.filter(follower_relations__following=user)
    following_users = User.objects.filter(following_relations__follower=user)

    # Check if the logged-in user is following the profile user
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()


    # Fetch reels uploaded by the user
    reels = Reel.objects.filter(user=user).order_by('-created_at')  # Get reels ordered by date created


    context = {
        'user': user,
        'profile': profile,
        'posts': Post.objects.filter(user=user),
        'followers_users': followers_users,
        'following_users': following_users,
        'is_following': is_following,  # Pass this to template
        'reels': reels,  # Pass reels to template
    }

    return render(request, 'posts/profile.html', context)


def create_post(request):
    if request.method == 'POST':
        caption = request.POST.get('caption', '')  # Default to empty string if missing
        hashtags = request.POST.get('hashtags', '')  # Use .get() to prevent errors
        
        # Save the post
        post = Post.objects.create(caption=caption, hashtags=hashtags, user=request.user)

        # Handle single image upload
        if 'single_image' in request.FILES:
            single_image = request.FILES['single_image']
            PostImage.objects.create(post=post, image=single_image)

        # Handle multiple images upload
        if 'multiple_images' in request.FILES:
            for image in request.FILES.getlist('multiple_images'):
                PostImage.objects.create(post=post, image=image)

        return redirect('home')

    return render(request, 'posts/create_post.html')




@login_required
def edit_profile(request):
    # Try to fetch the user's profile
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
        profile.save()  # Create the profile if it doesn't exist

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # Save the form data, which will update the profile
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=profile)

    context = {
        'form': form,
        'profile': profile
    }
    
    return render(request, 'posts/edit_profile.html', context)


# def profile(request, username):
#     try:
#         user = User.objects.get(username=username)
#         profile = user.profile  # This will raise DoesNotExist if no profile is created
#     except Profile.DoesNotExist:
#         profile = None  # or create a default profile object
#     except User.DoesNotExist:
#         return redirect('home')  # Redirect if user is not found
    
#     context = {
#         'user': user,
#         'profile': profile,
#         'posts': Post.objects.filter(user=user)
    
#     }
    
#     return render(request, 'posts/profile.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)  # Ensure only the owner can delete
    post.delete()
    return redirect('home')  # Redirect to home after deletion



@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        text = request.POST.get('text')
        if text:
            Comment.objects.create(post=post, user=request.user, text=text)
    return redirect('profile', username=post.user.username)



@login_required
def delete_comment(request, comment_id):
    # Debugging line: Check the comment_id received
    print(f"Trying to delete comment with ID: {comment_id}")

    # Try to retrieve the comment
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the current user is the comment owner or an admin
    if request.user == comment.user or request.user.is_superuser:
        post = comment.post  # Get the post related to the comment
        comment.delete()

        # Redirect to the profile page of the post's author
        return redirect('profile', username=post.user.username)

    return HttpResponseForbidden("You are not allowed to delete this comment.")




# def edit_post(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
    
#     # Ensure that only the owner can edit the post
#     if request.user != post.user:
#         return redirect('home')  # Redirect to home or an error page if not the post owner

#     if request.method == 'POST':
#         # Get the form data
#         caption = request.POST.get('caption')
#         hashtags = request.POST.get('hashtags')
#         new_image = request.FILES.get('image')  # Get the new image if uploaded

#         # Update the post instance with new data
#         post.caption = caption
#         post.hashtags = hashtags

#         # If there's a new image, update it
#         if new_image:
#             post.image = new_image

#         post.save()
#         return redirect('profile', username=request.user.username)  # Redirect after saving changes

#     return render(request, 'posts/edit_post.html', {'post': post})  


# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Post, PostImage
# from django.core.files.storage import default_storage

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.user:
        return redirect('home')  # Prevent unauthorized access

    if request.method == "POST":
        caption = request.POST.get("caption")
        hashtags = request.POST.get("hashtags")
        new_images = request.FILES.getlist("images")  # Get multiple uploaded images

        # Update text fields
        post.caption = caption
        post.hashtags = hashtags
        post.save()

        # If new images are uploaded, delete old images and save new ones
        if new_images:
            # Delete old images
            post.images.all().delete()  

            # Save new images
            for image in new_images:
                PostImage.objects.create(post=post, image=image)

        return redirect('profile', post.user.username)


    return render(request, "posts/edit_post.html", {"post": post})




def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({"liked": liked, "total_likes": post.total_likes()})


# follow unfollow
# @login_required
# def follow_unfollow(request, username):
#     user_to_follow = get_object_or_404(User, username=username)
#     profile_to_follow = user_to_follow.profile
#     current_user_profile = request.user.profile  # Get the current user's profile

#     if request.user in profile_to_follow.followers.all():
#         # Unfollow
#         profile_to_follow.followers.remove(request.user)
#         current_user_profile.following.remove(user_to_follow)
#     else:
#         # Follow
#         profile_to_follow.followers.add(request.user)
#         current_user_profile.following.add(user_to_follow)

#     return redirect("profile", username=username)


@login_required
def follow_unfollow(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if user_to_follow == request.user:
        return redirect("profile", username=username)  # Prevent self-follow

    # Check if the current user already follows the target user
    existing_follow = Follow.objects.filter(follower=request.user, following=user_to_follow)

    if existing_follow.exists():
        existing_follow.delete()  # Unfollow
    else:
        Follow.objects.create(follower=request.user, following=user_to_follow)  # Follow

    return redirect("profile", username=username)






# reels


@login_required
def create_reel(request):
    if request.method == "POST":
        video = request.FILES.get("video")
        caption = request.POST.get("caption", "")
        if video:
            Reel.objects.create(user=request.user, video=video, caption=caption)
        return redirect("reels_feed")

    return render(request, "posts/create_reel.html")

@login_required
def reels_feed(request):
    reels = Reel.objects.all().order_by('-created_at')
    return render(request, 'posts/reels.html', {'reels': reels})

@login_required
def like_reel(request, reel_id):
    reel = get_object_or_404(Reel, id=reel_id)

    # Check if the user has already liked the reel
    if reel.likes.filter(id=request.user.id).exists():
        reel.likes.remove(request.user)  # Unlike
        liked = False
    else:
        reel.likes.add(request.user)  # Like
        liked = True

    # Return JSON response with updated like count and status
    return JsonResponse({
        "liked": liked,
        "likes_count": reel.likes.count()
    })


@login_required
def add_reel_comment(request, reel_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Extract JSON data
            comment_text = data.get("comment_text")  # Ensure this matches the JS request key

            if not comment_text:
                return JsonResponse({"error": "Comment cannot be empty"}, status=400)

            reel = Reel.objects.get(id=reel_id)
            comment = ReelComment.objects.create(user=request.user, reel=reel, text=comment_text)
            
            return JsonResponse({"comment": comment.text, "user": comment.user.username})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def delete_reel(request, reel_id):
    print(f"Received DELETE request for reel_id: {reel_id}")  # Debugging Log

    if request.method == "POST":
        try:
            reel = get_object_or_404(Reel, id=reel_id)
            if reel.user != request.user:
                return JsonResponse({"success": False, "error": "Unauthorized"}, status=403)
            
            reel.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            print(f"Error deleting reel: {e}")  # Debugging Log
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


@login_required
def delete_reel_comment(request, comment_id):
    comment = get_object_or_404(ReelComment, id=comment_id)

    # Ensure only the comment's author can delete it
    if comment.user != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    comment.delete()
    return JsonResponse({"success": True})




# This will simulate a message store in memory
message_store = {}


@login_required
def chatbox(request):
    # Get the user id from the query string or POST data
    user_id = request.GET.get('user')
    
    if request.method == 'POST':
        # Process the form submission
        message_content = request.POST.get('message')
        
        # Get the selected user and current user
        selected_user = CustomUser.objects.get(id=user_id)
        sender = request.user
        
        # Create a new message
        Message.objects.create(
            sender=sender,
            receiver=selected_user,
            message=message_content,
        )
        
        # After sending a message, redirect to the chatbox with the selected user
        return HttpResponseRedirect(f'/chatbox/?user={user_id}')

    # Get the users the current user is following
    following_users = request.user.following_relations.all().values_list('following', flat=True)
    users_to_chat = CustomUser.objects.filter(id__in=following_users)
    
    # Get the selected user for the chat
    selected_user = CustomUser.objects.filter(id=user_id).first() if user_id else None

    # Get the messages between the current user and selected user
    # Ensure messages are ordered by timestamp
    messages = Message.objects.filter(
        sender__in=[request.user, selected_user], 
        receiver__in=[request.user, selected_user]
    ).order_by('timestamp')

    return render(request, 'posts/chatbox.html', {
        'users_to_chat': users_to_chat,
        'selected_user': selected_user,
        'messages': messages
    })


@login_required
def delete_message(request, message_id):
    # Ensure that only the sender can delete the message
    message = get_object_or_404(Message, id=message_id)
    
    if message.sender == request.user:
        message.delete()

    # Get the selected user ID from the query string
    user_id = request.GET.get('user')

    # If no user_id is found in the URL, it could be a direct visit to the URL without any query parameter
    if not user_id:
        # In case no 'user' param is found, we can either return to the home page or a fallback
        return redirect('home')

    # Redirect back to the same chatbox page with the same user_id
    return redirect(f'/chatbox/?user={user_id}')






# story 


@login_required
@login_required
def upload_story(request):
    user = request.user
    user_has_active_story = Story.objects.filter(user=user, created_at__gte=now() - timedelta(hours=24)).exists()

    if request.method == 'POST' and request.FILES.get('media'):
        if user_has_active_story:
            print(f"{user.username} already has an active story!")
            return redirect('upload_story')  # Prevent re-upload if an active story exists

        media = request.FILES['media']
        print(f"Uploading new story for {user.username}")

        # Delete existing story before saving a new one
        Story.objects.filter(user=user).delete()

        # Create a new story
        Story.objects.create(user=user, media=media)

        return redirect('home')

    return render(request, 'posts/upload_story.html', {'user_has_active_story': user_has_active_story})



@login_required
def view_story(request, story_id):
    story = Story.objects.get(id=story_id)

    # Check if the story is expired
    if story.is_expired():
        return redirect('home')

    return render(request, 'posts/view_story.html', {'story': story})




class Command(BaseCommand):
    help = 'Delete expired stories'

    def handle(self, *args, **kwargs):
        expired_stories = Story.objects.filter(created_at__lt=timezone.now() - timezone.timedelta(hours=24))
        expired_stories.delete()




@login_required
def delete_story(request, story_id):
    story = get_object_or_404(Story, id=story_id, user=request.user)

    if request.method == 'POST':
        story.delete()
        return redirect('home')  # Redirect to home after deletion

    return redirect('view_story', story_id=story_id)  # If accessed via GET, redirect back