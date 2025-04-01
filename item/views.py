from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Item, Category
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, EditItemForm
from django.db.models import Q

def items(request):
    # Pobierz parametry z żądania
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort_by', '')

    # Bazowe zapytanie
    items = Item.objects.filter(price__gt=1)

    # Filtrowanie po kategorii
    if category_id:
        items = items.filter(category_id=category_id)

    # Filtrowanie po nazwie lub opisie
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Filtrowanie po cenie minimalnej
    if min_price:
        try:
            min_price = float(min_price)
            items = items.filter(price__gte=min_price)
        except ValueError:
            pass

    # Filtrowanie po cenie maksymalnej
    if max_price:
        try:
            max_price = float(max_price)
            items = items.filter(price__lte=max_price)
        except ValueError:
            pass

    # Sortowanie
    if sort_by == 'price_asc':
        items = items.order_by('price')
    elif sort_by == 'price_desc':
        items = items.order_by('-price')
    elif sort_by == 'newest':
        items = items.order_by('-created_at')
    elif sort_by == 'oldest':
        items = items.order_by('created_at')
    else:
        items = items.order_by('?')  # domyślnie losowo

    # Pobierz kategorie
    categories = Category.objects.all()

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    })


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html',{
        'item': item,
        'related_items': related_items
    })

@login_required
def new(request):
    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Nowe ogłoszenie'
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')


@login_required
def edit(request,pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == "POST":
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edytuj przedmiot'
    })