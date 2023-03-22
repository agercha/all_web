from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.dateparse import parse_datetime
import datetime

from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from socialnetwork.forms import *
from socialnetwork.models import *

import json

def _my_json_error_response(message, status=200):
  # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
  response_json = '{ "error": "' + message + '" }'
  return HttpResponse(response_json, content_type='application/json', status=status)

# @login_required
def get_json_stream_help(request, isfollower):
  if not request.user.id or not request.user.email:
    return _my_json_error_response("You must be logged in to do this operation", status=401)
  current_user = Profile.objects.get(user=request.user)
  response_data = []
  for model_post in Post.objects.all():
    if model_post.author in current_user.friends.all() or not isfollower:
      comments = list(Comment.objects.filter(post=model_post.id))
      comments_list = []
      for comment in comments:
        comment_dict = {
          'id': comment.id,
          'content': str(comment.content),
          'date_time': comment.date_time.isoformat(),
          # 'date_time': comment.date_time.strftime("%m/%d/%Y %I:%M %p"),
          'author_first_name': comment.author.first_name,
          'author_last_name': comment.author.last_name,
          'author': comment.author.username,
        }
        comments_list.append(comment_dict)
      my_item = {
        'id': model_post.id,
        'content': str(model_post.content),
        'date_time': model_post.date_time.isoformat(),
        # 'date_time': model_post.date_time.strftime("%m/%d/%Y %I:%M %p"),
        'author_first_name': model_post.author.first_name,
        'author_last_name': model_post.author.last_name,
        'author': model_post.author.username,
        'comments': comments_list
      }
      response_data.append(my_item)

  response_json = json.dumps(response_data)
  response = HttpResponse(response_json, content_type='application/json')
  response['Access-Control-Allow-Origin'] = '*'
  return response

# @login_required
def get_json_stream(request):
  if not request.user.id or not request.user.email:
    return _my_json_error_response("You must be logged in to do this operation", status=401)
  return get_json_stream_help(request, False)

# @login_required
def get_json_friend_stream(request):
  if not request.user.id or not request.user.email:
    return _my_json_error_response("You must be logged in to do this operation", status=401)
  return get_json_stream_help(request, True)

@login_required
def global_stream(request):
  return render(request, 'socialnetwork/home.html', {})

@login_required
def global_stream_post(request):
  print(request.user)
  if not request.user.id or not request.user.email:
    return _my_json_error_response("You must be logged in to do this operation", status=401)

  if request.method != 'POST':
    return _my_json_error_response("You must use a POST request for this operation", status=405)

  if not 'post_text' in request.POST or not request.POST['post_text']:
    return _my_json_error_response("You must enter an item to add.", status=400)
  
  post = Post()

  post.author = request.user
  post.date_time = timezone.now()
  print(post.date_time)
  post.content = request.POST['post_text']
  post.save()
  return get_json_stream(request)

# @login_required
def global_stream_comment(request):
  # deal with friend stream comment
  if not request.user.id or not request.user.email:
    return _my_json_error_response("You must be logged in to do this operation", status=401)

  if request.method != 'POST':
    return _my_json_error_response("You must use a POST request for this operation", status=405)

  if not 'comment_text' in request.POST or not request.POST['comment_text']:
    return _my_json_error_response("You must enter an item to add.", status=400)

  if not 'post_id' in request.POST or not request.POST['post_id']:
    return _my_json_error_response("Post id missing", status=400)

  else:
    try:
      if int(request.POST['post_id']) > len(Post.objects.all()):
        return _my_json_error_response("Post Id is too large", status=400)
    except:
      return _my_json_error_response("Invalid post id", status=400)

  comment = Comment()

  comment.author = request.user
  comment.date_time = timezone.now()
  comment.content = request.POST['comment_text']
  comment.post = request.POST['post_id']
  comment.save()

  # return global_stream(request)
  return get_json_stream(request)

# @login_required
def friend_stream_comment(request):
  # deal with friend stream comment
  if not request.user.id or not request.user.email:
    return _my_json_error_response("You must be logged in to do this operation", status=401)

  if request.method != 'POST':
    return _my_json_error_response("You must use a POST request for this operation", status=405)

  if not 'comment_text' in request.POST or not request.POST['comment_text']:
    return _my_json_error_response("You must enter an item to add.", status=400)

  if not 'post_id' in request.POST or not request.POST['post_id']:
    return _my_json_error_response("Post id missing", status=400)

  else:
    try:
      if int(request.POST['post_id']) > len(Post.objects.all()):
        return _my_json_error_response("Post Id is too large", status=400)
    except:
      return _my_json_error_response("Invalid post id", status=400)

  comment = Comment()

  comment.author = request.user
  comment.date_time = timezone.now()
  comment.content = request.POST['comment_text']
  comment.post = request.POST['post_id']
  comment.save()

  return get_json_friend_stream(request)

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
  return render(request, 'socialnetwork/friend.html', {})

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
    print(request.user.id)
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
    return redirect(reverse('get-global'))

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
  return redirect(reverse('get-global'))

def logout_action(request):
  logout(request)
  return redirect(reverse('login'))


def get_posts_django_serializer(request):
  response_json = serializers.serialize('json', Post.objects.all())
  return HttpResponse(response_json, content_type='application/json')


def get_posts_xml(request):
    response_json = serializers.serialize('xml', Post.objects.all())
    return HttpResponse(response_json, content_type='application/xml')


def get_posts_xml_template(request):
    context = { 'items': Post.objects.all() }
    return render(request, 'socialnetwork/post.xml', context, content_type='application/xml')