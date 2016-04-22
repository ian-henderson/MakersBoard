from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import UserForm, UserUpdateForm, UserLoginForm
from .models import UserProfile


def user_login(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return HttpResponseRedirect(user.get_absolute_url())
        else:
            messages.error(request, 'Invalid login credentials.')
    context = {
        'form': form,
    }
    return render(request, 'user_login.html', context)


def user_logout(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return HttpResponseRedirect('/posts')


def user_create(request):  # CRUD: Create
    form = UserForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # Get necessary data from form
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        # Create User
        user = UserProfile.objects.create_user(username, email, password)
        # Get rest of data for user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.profile_picture = form.cleaned_data['profile_picture']
        user.phone_number = form.cleaned_data['phone_number']
        # Save info
        user.save()
        messages.success(request, 'Successfully created user.')
        # Log new user in
        # logout(request)
        user_auth = authenticate(username=username, password=password)
        login(request, user_auth)
        messages.success(request, 'Successfully logged in.')
        return HttpResponseRedirect(user.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'user_form.html', context)


def user_update(request, slug=None):
    user = get_object_or_404(UserProfile, slug=slug)
    form = UserUpdateForm(request.POST or None, request.FILES or None,
                          instance=user)
    if form.is_valid():
        # Get new user info
        user.profile_picture = form.cleaned_data['profile_picture']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.phone_number = form.cleaned_data['phone_number']
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(request, 'Successfully updated user.')
        return HttpResponseRedirect(user.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'user_update_form.html', context)


def user_list(request):
    queryset_list = UserProfile.objects.all()
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
    context = {
        'instance': instance,
    }
    return render(request, 'user_detail.html', context)


def user_delete(request, slug=None):  # CRUD: Delete
    instance = get_object_or_404(UserProfile, slug=slug)
    instance.delete()
    messages.success(request, 'Successfully deleted user.')
    return redirect('users:list')
