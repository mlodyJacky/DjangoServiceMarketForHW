from django.shortcuts import render, redirect
from django.contrib.auth import logout
from item.models import Category, Item
from core.utils import get_client_ip
from .forms import SignupForm
from user.models import Profile
# Create your views here.

def index(request):
    items = Item.objects.filter(price__gt=1).order_by('?')[0:8]
    categories = Category.objects.all()
    return render(request, 'core/index.html', {
                  'categories': categories,
                  'items': items,
                  })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            ip = get_client_ip(request)

            if Profile.objects.filter(registration_ip=ip).exists():
                form.add_error(None, 'Z tego adresu IP utworzono już konto.')
            else:
                user = form.save()
                user.profile.registration_ip = ip
                user.profile.save()
                return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })



def logout_view(request):
    logout(request)
    return redirect('core:index')