from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


from socialnetwork.forms import LoginForm, RegisterForm

def stream(request, type):
  if type == "global":
    dummy_posts = [{"content": "I ate lunch", "id":"1", "user":"alice", "time": "9/25/2022 1:00 PM",
                    "comments":[{"content":"ok? and?", "id":"id_comment_div_1", "user":"alice", "time": "9/25/2022 1:05 PM"}, 
                                {"content":"whatevr", "id":"id_comment_div_2", "user":"alice", "time": "9/25/2022 1:07 PM"}]}, 
                {"content": "go pats!", "id":"2", "user":"alice", "time": "9/25/2022 1:30 PM"}, 
                {"content": "yuh-uh", "id":"3", "user":"alice", "time": "9/25/2022 1:34 PM"}, 
                {"content": "nuh-uh", "id":"4", "user":"alice", "time": "9/25/2022 1:40 PM"}]
    context = {"posts":dummy_posts, "new_post":["dummy"], "page_name":"GLOBAL STREAM"}
  else:
    dummy_posts = [{"content": "I ate lunch", "id":"1", "user":"alice", "time": "9/25/2022 1:00 PM",
                    "comments":[{"content":"ok? and?", "id":"id_comment_div_1", "user":"alice", "time": "9/25/2022 1:05 PM"}, 
                                {"content":"whatevr", "id":"id_comment_div_2", "user":"alice", "time": "9/25/2022 1:07 PM"}]}, 
                {"content": "go pats!", "id":"2", "user":"alice", "time": "9/25/2022 1:30 PM"}]
    context = {"posts":dummy_posts, "page_name":"FOLLOWER STREAM"}
  return render(request, 'socialnetwork/home.html', context)

@login_required
def global_stream(request):
  return stream(request, "global")

@login_required
def friend_stream(request):
  return stream(request, "friend")

@login_required
def dummy_profile(request):
  context = {"user_bio": "I am definitely not you!!", 
      "header" : "profile page for dummy", "follow_status": "unfollow",
      "picture_src": "static/socialnetwork/annagerchanovskyhead_flipped.jpeg"}
  return render(request, 'socialnetwork/user.html', context)


@login_required
def users_profile(request):
  context = {"user_bio": "Hello, I am you!",
      "friends": [{"link":"dummy", "name":"Alice", "id":"1"}],
      "picture_src": "static/socialnetwork/annagerchanovskyhead.jpeg"}
  return render(request, 'socialnetwork/self.html', context)

def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        print("A")
        print(context)
        return render(request, 'socialnetwork/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form
    print("B")
    print(context)
    print(dir(context['form']))
    print((context['form']).non_field_errors())
    print(dir(context['form'].fields["username"]))
    print(dir(context['form'].fields["password"]))
    print((context['form'].fields["username"]).error_messages)
    print((context['form'].fields["password"]).error_messages)
    # print(context['form'].fields[0].errors)
    # print(context['form'].fields[1].errors)
    print(context['form'].visible_fields()[0].errors)
    print(context['form'].visible_fields()[1].errors)

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

  login(request, new_user)
  return redirect(reverse('home'))

def logout_action(request):
  logout(request)
  return redirect(reverse('login'))