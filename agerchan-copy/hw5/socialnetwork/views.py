from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from socialnetwork.forms import *
from socialnetwork.models import *

def stream(request, type):
  current_user = Profile.objects.get(user=request.user)
  posts = reversed(Post.objects.all())
  post_array = []
  for post in posts:
    post_id = post.id
    comments = list(Comment.objects.filter(post=post_id))
    post.comments = comments
    if type == "global" or post.author in current_user.friends.all():
      post_array.append(post)
  if type == "global":
    context = {"posts": post_array, "new_post":True, "page_name":"GLOBAL STREAM"}
  else:
    context = {"posts":post_array, "page_name":"FOLLOWER STREAM"}
  return render(request, 'socialnetwork/home.html', context)

@login_required
def global_stream(request):
  if request.method == 'POST':
    post = Post()

    post.author = request.user
    post.date_time = timezone.now()
    post.content = request.POST['post_input_text']

  return stream(request, "global")

@login_required
def global_stream_post(request):
  if request.method == 'POST':
    post = Post()

    post.author = request.user
    post.date_time = timezone.now()
    post.content = request.POST['post_input_text']
    post.save()

  return stream(request, "global")

@login_required
def global_stream_comment(request):
  if request.method == 'POST':
    comment = Comment()

    comment.author = request.user
    comment.date_time = timezone.now()
    comment.content = request.POST['post_input_text']
    comment.post = request.POST['comment_post']
    comment.save()
  return stream(request, "global")


@login_required
def get_self_pfp(request):
  current_user = Profile.objects.get(user=request.user)
  pfp = current_user.profile_pic
  
  return HttpResponse(pfp, content_type=current_user.pfp_type)

@login_required
def get_pfp(request, author):
  user = User.objects.get(username=author)
  current_user = Profile.objects.get(user=user)
  pfp = current_user.profile_pic
  
  return HttpResponse(pfp, content_type=current_user.pfp_type)

@login_required
def friend_stream(request):
  return stream(request, "friend")

@login_required
def follow_unfollow(request, other_username):
  current_user = Profile.objects.get(user=request.user)
  other_user = User.objects.get(username=other_username)
  if other_user in current_user.friends.all():
    current_user.friends.remove(other_user)
  else:
    current_user.friends.add(other_user)
  return other_profile(request, other_username)

@login_required
def other_profile(request, author):
  if author == request.user.username:
    return users_profile(request)
  else:
    current_user = Profile.objects.get(user=request.user)
    other_user = User.objects.get(username=author)
    if other_user in current_user.friends.all():
      follow_status="unfollow"
    else:
      follow_status="follow"
    current_user = Profile.objects.get(user=other_user)
    context = {"other_user": other_user,
        "user_bio": current_user.bio, 
        "header" : f"profile page for {current_user}", 
        "follow_status": follow_status}
    return render(request, 'socialnetwork/user.html', context)

@login_required
def users_profile(request):
  current_user = Profile.objects.get(user=request.user)
  if request.method == 'POST':
    form = ProfileForm(request.POST, request.FILES, instance=current_user)
    if form.is_valid():
      current_user.bio = form.cleaned_data['bio']
      current_user.profile_pic = form.clean_picture()
      current_user.pfp_type = (form.cleaned_data['profile_pic']).content_type
      form.save()

  user_pfp = current_user.profile_pic
  friends = list(current_user.friends.all())
  context = {"user_pfp": user_pfp,
      "user_bio": current_user.bio,
      "friends": friends,
      "profile_form": ProfileForm(initial={'bio': current_user.bio})}

  return render(request, 'socialnetwork/self.html', context)

def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))

def register_action(request):
  context = {}

  # Just display the registration form if this is a GET request.
  if request.method == 'GET':
      context['form'] = RegisterForm()
      return render(request, 'socialnetwork/register.html', context)

  # Creates a bound form from the request POST parameters and makes the 
  # form available in the request context dictionary.
  form = RegisterForm(request.POST)
  context['form'] = form

  # Validates the form.
  if not form.is_valid():
      return render(request, 'socialnetwork/register.html', context)

  # At this point, the form data is valid.  Register and login the user.
  new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                      password=form.cleaned_data['password'],
                                      email=form.cleaned_data['email'],
                                      first_name=form.cleaned_data['first_name'],
                                      last_name=form.cleaned_data['last_name'])
  new_user.save()

  new_user = authenticate(username=form.cleaned_data['username'],
                          password=form.cleaned_data['password'])

  # new_pfp = PFP(pfp_user=form.cleaned_data['username'])
  # new_pfp.save()
  new_user_profile = Profile(user=new_user, 
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            bio="")
  new_user_profile.save()

  login(request, new_user)
  return redirect(reverse('home'))

def logout_action(request):
  logout(request)
  return redirect(reverse('login'))