from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from user.models import Profile
import random

def search_users(request):
    query = request.GET.get('q', '')
    seed = request.GET.get('seed')

    if not seed:
        seed = str(random.randint(0, 999999))
    
    if query:
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.all()

    users = list(users)
    random.Random(seed).shuffle(users)

    paginator = Paginator(users, 6)  # 6 użytkowników na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    profiles = Profile.objects.filter(user__in=page_obj.object_list)

    return render(request, 'users/items.html', {
        'query': query,
        'profiles': profiles,
        'page_obj': page_obj,
        'seed': seed,
    })
