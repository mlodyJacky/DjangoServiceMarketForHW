from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from user.models import Profile

from user.models import Profile
from user.forms import ProfileUpdateForm


from conversation.models import Conversation
from conversation.forms import ConversationMessageForm
from item.models import Item


def search_users(request):
    query = request.GET.get('q', '') 
    
    if query:
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.all()[:9] 
    
    profiles = Profile.objects.filter(user__in=users)

    return render(request, 'users/items.html', {'profiles': profiles, 'query': query})
