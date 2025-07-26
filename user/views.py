from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileUpdateForm
from item.models import Item

@login_required
def profile_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    items = Item.objects.filter(created_by=profile.user)

    if request.user == profile.user:
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('user:profile', username=username)
        else:
            form = ProfileUpdateForm(instance=profile)
    else:
        form = None  # Inni użytkownicy nie mogą edytować

    return render(request, 'user/profile.html', {
        'profile': profile,
        'form': form,
        'items': items,
    })