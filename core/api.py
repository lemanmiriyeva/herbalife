import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Case, When, F, DecimalField
from django.shortcuts import get_object_or_404
from .models import Store, ProductStore

from .models import Category, Product, Cart, CartItem


# ── Helpers ──────────────────────────────────────────────────────

def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

def cart_to_dict(cart, request=None):
    items = []
    for item in cart.items.select_related('product__category').all():
        items.append({
            'id':       item.pk,
            'quantity': item.quantity,
            'subtotal': str(item.subtotal),
            'product':  product_to_dict(item.product, request),
        })
    return {
        'id':          cart.pk,
        'total_items': cart.total_items,
        'total_price': str(cart.total_price),
        'items':       items,
    }


# ── Categories ───────────────────────────────────────────────────

def categories(request):
    """GET /api/categories/"""
    data = list(Category.objects.values('id', 'name', 'slug'))
    return JsonResponse(data, safe=False)


# ── Products ─────────────────────────────────────────────────────

def get_active_store(request):
    """request.store mövcuddursa onu, yoxsa default AZ store-u qaytar"""
    store = getattr(request, 'store', None)
    if store:
        return store
    return Store.objects.filter(is_active=True).first()
 
 
def product_to_dict(p, request=None, store=None):
    """store_price-i store-a görə götür"""
    if store is None and request is not None:
        store = get_active_store(request)
 
    # Bu store-da ProductStore var mı?
    try:
        sp = p.store_prices.get(store=store)
        price          = str(sp.price)
        discount_price = str(sp.discount_price) if sp.discount_price else None
        final_price    = str(sp.final_price)
        in_stock       = sp.stock
    except (ProductStore.DoesNotExist, AttributeError):
        # Fallback: məhsulun öz qiyməti
        price          = str(p.price)
        discount_price = str(p.discount_price) if p.discount_price else None
        final_price    = str(p.final_price)
        in_stock       = p.stock
 
    return {
        'id':            p.pk,
        'name':          p.name,
        'slug':          p.slug,
        'size':          p.size,
        'flavor_name':   p.flavor_name,
        'flavor_color':  p.flavor_color,
        'badge':         p.badge,
        'description':   p.description,
        'price':         price,
        'discount_price': discount_price,
        'final_price':   final_price,
        'price_note':    p.price_note,
        'is_addable':    p.is_addable,
        'image':         request.build_absolute_uri(p.image.url) if (p.image and request) else (p.image.url if p.image else None),
        'stock':         in_stock,
        'is_featured':   p.is_featured,
        'category':      {'id': p.category.pk, 'name': p.category.name, 'slug': p.category.slug} if p.category else None,
        'created_at':    p.created_at.isoformat(),
        # Store info
        'store': {
            'code':     store.code     if store else 'AZ',
            'currency': store.currency if store else 'AZN',
        } if store else None,
    }
 
 
def products(request):
    """Store-a görə filtrlənmiş məhsullar"""
    store = get_active_store(request)
 
    # Yalnız bu store-da aktiv olan məhsulları çək
    qs = Product.objects.filter(
        is_active=True,
        store_prices__store=store,
        store_prices__is_active=True,
    ).select_related('category').prefetch_related('store_prices__store').distinct()
 
    # Mövcud filter/sort məntiqi eyni qalır...
    cat_slug = request.GET.get('category', '').strip()
    if cat_slug:
        qs = qs.filter(category__slug=cat_slug)
 
    if request.GET.get('featured'):
        qs = qs.filter(is_featured=True)
 
    q = request.GET.get('search', '').strip()
    if q:
        qs = qs.filter(
            Q(name__icontains=q) | Q(description__icontains=q) |
            Q(flavor_name__icontains=q) | Q(category__name__icontains=q)
        ).distinct()
 
    sort_map = {
        'price_asc':  'price', 'price_desc': '-price',
        'name_asc':   'name',  'name_desc':  '-name',
    }
    qs = qs.order_by(sort_map.get(request.GET.get('sort', ''), '-created_at'))
 
    return JsonResponse([product_to_dict(p, request, store) for p in qs], safe=False)
 
 
def store_switch(request):
    """POST /api/store/switch/  body: {store_code: "US"}"""
    import json
    try:
        body = json.loads(request.body)
        code = body.get('store_code', '').upper()
        store = Store.objects.get(code=code, is_active=True)
        request.session['store_code'] = store.code
        return JsonResponse({
            'success': True,
            'store': {
                'code':     store.code,
                'name':     store.name,
                'currency': store.currency,
            }
        })
    except Store.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Store not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
 
 
def store_info(request):
    """GET /api/store/ — aktiv store məlumatı"""
    store = get_active_store(request)
    all_stores = Store.objects.filter(is_active=True).values('code', 'name', 'currency')
    return JsonResponse({
        'active': {
            'code':     store.code,
            'name':     store.name,
            'currency': store.currency,
        } if store else None,
        'all': list(all_stores),
    })

def product_detail(request, slug):
    """GET /api/products/<slug>/"""
    p = get_object_or_404(Product, slug=slug, is_active=True)
    data = product_to_dict(p, request)
    # Related products
    related = Product.objects.filter(
        category=p.category, is_active=True
    ).exclude(pk=p.pk).select_related('category')[:4]
    data['related'] = [product_to_dict(r, request) for r in related]
    return JsonResponse(data)


def search_suggest(request):
    """GET /api/search/suggest/?q=<query>  — live search, min 2 chars"""
    q = request.GET.get('q', '').strip()
    results = []
    if len(q) >= 2:
        qs = Product.objects.filter(is_active=True).filter(
            Q(name__icontains=q) | Q(category__name__icontains=q)
        ).select_related('category')[:8]
        results = [product_to_dict(p, request) for p in qs]
    return JsonResponse({'query': q, 'results': results})


# ── Cart ─────────────────────────────────────────────────────────

def cart_get(request):
    """GET /api/cart/"""
    cart = get_or_create_cart(request)
    return JsonResponse(cart_to_dict(cart, request))


@csrf_exempt
def cart_add(request):
    """POST /api/cart/add/   body: {product_id, quantity}"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        body = json.loads(request.body)
    except Exception:
        body = {}

    product_id = body.get('product_id') or request.POST.get('product_id')
    quantity   = int(body.get('quantity', 1) or request.POST.get('quantity', 1))

    product = get_object_or_404(Product, pk=product_id, is_active=True)
    if product.stock == 0:
        return JsonResponse({'error': 'Out of stock'}, status=400)

    quantity = min(max(1, quantity), product.stock)
    cart     = get_or_create_cart(request)

    item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, defaults={'quantity': quantity}
    )
    if not created:
        item.quantity = min(item.quantity + quantity, product.stock)
        item.save()

    return JsonResponse(cart_to_dict(cart, request))


@csrf_exempt
def cart_update(request, item_id):
    """PATCH /api/cart/items/<id>/   body: {quantity}"""
    if request.method not in ('PATCH', 'POST'):
        return JsonResponse({'error': 'PATCH required'}, status=405)
    try:
        body = json.loads(request.body)
    except Exception:
        body = {}

    quantity = int(body.get('quantity', 1))
    cart     = get_or_create_cart(request)
    item     = get_object_or_404(CartItem, pk=item_id, cart=cart)

    if quantity <= 0:
        item.delete()
    else:
        item.quantity = min(quantity, item.product.stock)
        item.save()

    return JsonResponse(cart_to_dict(cart, request))


@csrf_exempt
def cart_remove(request, item_id):
    """DELETE /api/cart/items/<id>/"""
    if request.method not in ('DELETE', 'POST'):
        return JsonResponse({'error': 'DELETE required'}, status=405)
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    item.delete()
    return JsonResponse(cart_to_dict(cart, request))


# ── Filters ──────────────────────────────────────────────────────

def filters(request):
    """
    GET /api/filters/
    DB-dən unikal flavor_name-lər, size-lar və qiymət aralıqları qaytarır.
    Products page sidebar-ı bunu çəkir.
    """
    from django.db.models import Min, Max

    qs = Product.objects.filter(is_active=True)

    # Unikal flavorlar (boş olmayanlar)
    flavors = list(
        qs.exclude(flavor_name='')
          .values_list('flavor_name', flat=True)
          .distinct()
          .order_by('flavor_name')
    )

    # Unikal size-lar (boş olmayanlar)
    sizes = list(
        qs.exclude(size='')
          .values_list('size', flat=True)
          .distinct()
          .order_by('size')
    )

    # Qiymət aralığı
    price_range = qs.aggregate(min=Min('price'), max=Max('price'))

    return JsonResponse({
        'flavors':     flavors,
        'sizes':       sizes,
        'price_min':   float(price_range['min'] or 0),
        'price_max':   float(price_range['max'] or 999),
    })


# ── Auth status ───────────────────────────────────────────────────

def auth_status(request):
    """GET /api/auth/status/ — istifadəçinin login olub-olmadığını qaytarır"""
    if request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True,
            'phone': request.user.phone,
            'name':  request.user.get_full_name(),
        })
    return JsonResponse({'authenticated': False})


# core/views.py-a əlavə et

from .models import BlogCategory, BlogPost

def blog_post_to_dict(post, request=None):
    return {
        'id':           post.pk,
        'title':        post.title,
        'slug':         post.slug,
        'excerpt':      post.excerpt,
        'body':         post.body,
        'cover_image':  request.build_absolute_uri(post.cover_image.url) if (post.cover_image and request) else (post.cover_image.url if post.cover_image else None),
        'cover_emoji':  post.cover_emoji,
        'author':       post.get_author_name(),
        'read_time':    post.read_time,
        'is_featured':  post.is_featured,
        'published_at': post.published_at.isoformat() if post.published_at else post.created_at.isoformat(),
        'category': {
            'id':   post.category.pk,
            'name': post.category.name,
            'slug': post.category.slug,
        } if post.category else None,
    }


def api_blog_posts(request):
    """GET /api/blog/posts/  ?cat=slug  ?search=q  ?featured=1"""
    from django.db.models import Q
    qs = BlogPost.objects.filter(is_published=True).select_related('category', 'author')

    cat_slug = request.GET.get('cat', '').strip()
    if cat_slug:
        qs = qs.filter(category__slug=cat_slug)

    if request.GET.get('featured'):
        qs = qs.filter(is_featured=True)

    q = request.GET.get('search', '').strip()
    if q:
        qs = qs.filter(
            Q(title__icontains=q) | Q(excerpt__icontains=q)
        ).distinct()

    return JsonResponse([blog_post_to_dict(p, request) for p in qs], safe=False)


def api_blog_post_detail(request, slug):
    """GET /api/blog/posts/<slug>/"""
    post    = get_object_or_404(BlogPost, slug=slug, is_published=True)
    data    = blog_post_to_dict(post, request)
    related = BlogPost.objects.filter(
        is_published=True, category=post.category
    ).exclude(pk=post.pk).select_related('category', 'author')[:3]
    data['related'] = [blog_post_to_dict(p, request) for p in related]
    return JsonResponse(data)


def api_blog_categories(request):
    """GET /api/blog/categories/"""
    cats = list(BlogCategory.objects.all().values('id', 'name', 'slug'))
    return JsonResponse(cats, safe=False)

def detect_location(request):
    """GET /api/location/ — IP-dən ölkəni tap"""
    import requests as req
    
    # Real IP-ni al (proxy arxasındasa)
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        ip = '8.8.8.8'
    else:
        ip = '8.8.8.8'
    
    try:
        # Server-dən server-ə sorğu — CORS yoxdur
        response = req.get(f'https://ipapi.co/{ip}/json/', timeout=3)
        data = response.json()
        country_code = data.get('country_code', 'AZ')
    except Exception:
        country_code = 'AZ'  # default
    
    return JsonResponse({'country_code': country_code})