import random
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Item, Category
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, EditItemForm
from django.db.models import Q

def items(request):
    query       = request.GET.get('query', '')
    category_id = request.GET.get('category', '')
    min_price   = request.GET.get('min_price', '')
    max_price   = request.GET.get('max_price', '')
    sort_by     = request.GET.get('sort_by', '')
    page_number = request.GET.get('page', '1')
    seed        = request.GET.get('seed')

    if not seed:
        seed = str(random.randint(0, 1_000_000_000))
        params = request.GET.copy()
        params['seed'] = seed
        params['page'] = '1'
        return redirect(f"{request.path}?{params.urlencode()}")

    qs = Item.objects.filter(price__gt=1)
    if category_id:
        qs = qs.filter(category_id=category_id)
    if query:
        qs = qs.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if min_price:
        try: qs = qs.filter(price__gte=float(min_price))
        except: pass
    if max_price:
        try: qs = qs.filter(price__lte=float(max_price))
        except: pass

    if sort_by == 'price_asc':
        qs = qs.order_by('price')
    elif sort_by == 'price_desc':
        qs = qs.order_by('-price')
    elif sort_by == 'newest':
        qs = qs.order_by('-created_at')
    elif sort_by == 'oldest':
        qs = qs.order_by('created_at')
    else:
        items_list = list(qs)
        random.Random(int(seed)).shuffle(items_list)
        qs = items_list

    paginator = Paginator(qs, 15)
    page_obj  = paginator.get_page(page_number)

    return render(request, 'item/items.html', {
        'items':        page_obj.object_list,
        'page_obj':     page_obj,
        'query':        query,
        'category_id':  category_id,
        'min_price':    min_price,
        'max_price':    max_price,
        'sort_by':      sort_by,
        'seed':         seed,
        'categories':   Category.objects.all(),
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category).exclude(pk=pk)[:3]
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

@login_required
def new(request):
    if request.method == "POST":
        form = NewItemForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm(request.user)
    return render(request, 'item/form.html', {'form': form, 'title': 'Nowe ogłoszenie'})

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    return redirect('dashboard:index')

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == "POST":
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
    return render(request, 'item/form.html', {'form': form, 'title': 'Edytuj przedmiot'})
