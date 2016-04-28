from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import UserForm, UserUpdateForm
from .models import UserProfile
from posts.models import Post


def user_login(request):
    if request.method == 'POST':
        auth_form = AuthenticationForm(request.POST)
        m = UserProfile.objects.get(username=request.POST['username'])
        if auth_form.is_valid:
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    # Session is created
                    request.session['member_id'] = m.id
                    login(request, user)
                    return HttpResponseRedirect('/posts')
    else:
        auth_form = AuthenticationForm()
    context = {
        'auth_form': auth_form,
    }
    return render(request, 'user_login.html', context)


def user_logout(request):
    try:
        logout(request)
        del request.session['member_id']
        messages.success(request, 'Logged out.')
    except KeyError:
        pass
    return HttpResponseRedirect('/posts')


def user_create(request):  # CRUD: Create
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid:
            # Create user
            user = UserProfile.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.full_name = "%s %s" % (request.POST['first_name'],
                                        request.POST['last_name'])
            user.profile_picture = request.FILES['profile_picture']
            user.phone_number = request.POST['phone_number']
            user.save()
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password'],
            )
            # Login
            login(request, user)
            messages.success(request, 'Logged in as %s.' % (user.username))
            return HttpResponseRedirect(user.get_absolute_url())
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'user_form.html', context)


def user_update(request, slug=None):  # CRUD: Update
    if request.method == 'POST':
        user = get_object_or_404(UserProfile, slug=slug)
        form = UserUpdateForm(request.POST or None, request.FILES or None,
                              instance=user)
        if form.is_valid:
            user.profile_picture = request.FILES['profile_picture']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.phone_number = request.POST['phone_number']
            user.save()
            messages.success(request, 'User %s updated.' % (user.username))
            return HttpResponseRedirect(user.get_absolute_url())
    else:
        form = UserUpdateForm()
    context = {
        'form': form,
    }
    return render(request, 'user_update_form.html', context)


def user_list(request):  # CRUD: Retrieve
    queryset_list = UserProfile.objects.filter(
        profile_picture__isnull=True,
    )
    paginator = Paginator(queryset_list, 10)  # Show 10 users per page
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        'object_list': queryset,
        'title': 'Maker\'s Board',
    }
    return render(request, 'user_list.html', context)


def user_detail(request, slug=None):  # CRUD: Retrieve
    instance = get_object_or_404(UserProfile, slug=slug)
    gallery = Post.objects.filter(user=instance)
    context = {
        'gallery': gallery,
        'instance': instance,
    }
    return render(request, 'user_detail.html', context)


def user_delete(request, slug=None):  # CRUD: Delete
    instance = get_object_or_404(UserProfile, slug=slug)
    username = instance.username
    instance.delete()
    messages.success(request, 'Successfully deleted user %s.' % (username))
    return redirect('users:list')
