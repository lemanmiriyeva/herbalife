# core/views.py — checkout bölməsini TAM bu ilə əvəz et
# (digər view-lar eyni qalır)

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Cart, CartItem, Order, OrderItem, Product, Wishlist, User
from .paypal_client import create_paypal_order, capture_paypal_order


# ── Helpers ───────────────────────────────────────────────────────

def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


# ── Page views ────────────────────────────────────────────────────

def home(request):           return render(request, 'home.html')
def products(request):       return render(request, 'products.html')
def product_detail(request, slug): return render(request, 'product-detail.html', {'slug': slug})
def cart(request):           return render(request, 'cart.html')
def blog(request):           return render(request, 'blogs.html')
def blog_detail(request, slug): return render(request, 'blog_detail.html', {'slug': slug})


# ── Auth ──────────────────────────────────────────────────────────

from django.db.models import Q

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()  # phone | email | username
        password   = request.POST.get('password', '')

        # Phone, email və ya username-dən birini tap
        try:
            user_obj = User.objects.get(
                Q(phone=identifier) |
                Q(email__iexact=identifier) |
                Q(username__iexact=identifier)
            )
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None
        except User.MultipleObjectsReturned:
            # Çox nadir hal — phone ilə tap
            try:
                user_obj = User.objects.get(phone=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'home'))

        return render(request, 'login.html', {
            'error':      'Məlumatlar yanlışdır və ya hesab tapılmadı.',
            'identifier': identifier,
        })

    return render(request, 'login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip().lower()
        phone      = request.POST.get('phone', '').strip()
        password   = request.POST.get('password', '')
        password2  = request.POST.get('password2', '')

        errors = {}

        if not first_name:
            errors['first_name'] = 'Ad daxil edin.'

        if not email:
            errors['email'] = 'E-poçt ünvanı daxil edin.'
        elif '@' not in email:
            errors['email'] = 'Düzgün e-poçt ünvanı daxil edin.'
        elif User.objects.filter(email__iexact=email).exists():
            errors['email'] = 'Bu e-poçt artıq qeydiyyatdan keçib.'

        if not phone:
            errors['phone'] = 'Telefon nömrəsi daxil edin.'
        elif User.objects.filter(phone=phone).exists():
            errors['phone'] = 'Bu nömrə artıq qeydiyyatdan keçib.'

        if len(password) < 6:
            errors['password'] = 'Şifrə ən az 6 simvol olmalıdır.'
        if password != password2:
            errors['password2'] = 'Şifrələr uyğun gəlmir.'

        if not errors:
            # Username = email-dən @ əvvəlki hissə + unikallıq yoxlaması
            base_username = email.split('@')[0].replace('.', '_')
            username = base_username
            counter  = 1
            while User.objects.filter(username=username).exists():
                username = f'{base_username}_{counter}'
                counter += 1

            user = User.objects.create_user(
                username   = username,
                email      = email,
                phone      = phone,
                first_name = first_name,
                last_name  = last_name,
                password   = password,
            )
            login(request, user)
            messages.success(request, 'Qeydiyyat uğurla tamamlandı!')
            return redirect(request.GET.get('next', 'home'))

        return render(request, 'register.html', {
            'errors':    errors,
            'form_data': request.POST,
        })

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('home')


# ── Profile ───────────────────────────────────────────────────────

@login_required(login_url='/login/')
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_info':
            user.first_name = request.POST.get('first_name', '').strip()
            user.last_name  = request.POST.get('last_name', '').strip()
            new_phone       = request.POST.get('phone', '').strip()
            if new_phone != user.phone and User.objects.filter(phone=new_phone).exclude(pk=user.pk).exists():
                messages.error(request, 'Bu telefon nömrəsi artıq istifadə edilir.')
            else:
                user.phone = new_phone
                user.save()
                messages.success(request, 'Məlumatlar yeniləndi.')
        elif action == 'update_address':
            user.address     = request.POST.get('address', '').strip()
            user.city        = request.POST.get('city', '').strip()
            user.postal_code = request.POST.get('postal_code', '').strip()
            user.country     = request.POST.get('country', '').strip()
            user.save()
            messages.success(request, 'Ünvan məlumatları yeniləndi.')
        elif action == 'change_password':
            old_pw  = request.POST.get('old_password', '')
            new_pw  = request.POST.get('new_password', '')
            new_pw2 = request.POST.get('new_password2', '')
            if not user.check_password(old_pw):
                messages.error(request, 'Köhnə şifrə yanlışdır.')
            elif len(new_pw) < 6:
                messages.error(request, 'Yeni şifrə ən az 6 simvol olmalıdır.')
            elif new_pw != new_pw2:
                messages.error(request, 'Şifrələr uyğun gəlmir.')
            else:
                user.set_password(new_pw)
                user.save()
                login(request, user)
                messages.success(request, 'Şifrə uğurla dəyişdirildi.')
        return redirect('profile')

    orders   = user.orders.prefetch_related('items').order_by('-created_at')[:10]
    wishlist = user.wishlist_items.select_related('product__category').order_by('-added_at')
    from .models import Store
    stores = Store.objects.filter(is_active=True)
    return render(request, 'profile.html', {'orders': orders, 'wishlist': wishlist, 'stores': stores})


# ── Wishlist ──────────────────────────────────────────────────────

# @login_required decorator-u SİL, manual yoxla
def wishlist_toggle(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'login_required', 'login_url': '/login/'}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        body = json.loads(request.body)
        product_id = body.get('product_id')
    except Exception:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    obj, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        obj.delete()
        in_wishlist = False
    else:
        in_wishlist = True
    return JsonResponse({'in_wishlist': in_wishlist, 'count': request.user.wishlist_items.count()})

def wishlist_status(request):
    if not request.user.is_authenticated:
        return JsonResponse({'wishlist_ids': [], 'count': 0})
    ids = list(request.user.wishlist_items.values_list('product_id', flat=True))
    return JsonResponse({'wishlist_ids': ids, 'count': len(ids)})

# ══════════════════════════════════════════════════════════════════
# CHECKOUT — Səbət → Ünvan → PayPal → Təsdiq
# ══════════════════════════════════════════════════════════════════

@login_required(login_url='/login/')
def checkout_address(request):
    """
    GET  → Ünvan forması göstər
    POST → Ünvanı session-a yaz, PayPal order yarat, redirect et
    """
    cart_obj = get_or_create_cart(request)
    items    = list(cart_obj.items.select_related('product').all())

    if not items:
        messages.warning(request, 'Səbətiniz boşdur.')
        return redirect('cart')

    # Store / currency
    from .models import Store
    from .api import get_active_store
    store    = get_active_store(request)
    currency = store.currency if store else 'USD'
    # PayPal yalnız USD/CAD qəbul edir — AZN-i USD-ə çevir (sabit kurs)
    CURRENCY_MAP = {'AZN': ('USD', 0.59), 'USD': ('USD', 1.0), 'CAD': ('CAD', 1.0)}
    pp_currency, rate = CURRENCY_MAP.get(currency, ('USD', 1.0))

    if request.method == 'POST':
        address     = request.POST.get('address', '').strip()
        city        = request.POST.get('city', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        country     = request.POST.get('country', '').strip()
        save_addr   = request.POST.get('save_address') == '1'
        note        = request.POST.get('note', '').strip()

        if not address or not city or not country:
            messages.error(request, 'Zəhmət olmasa ünvan məlumatlarını tam daxil edin.')
            return render(request, 'checkout_address.html', {
                'items': items, 'cart': cart_obj,
                'currency': currency, 'store': store,
                'form': request.POST,
            })

        # İstəsə ünvanı profildə saxla
        if save_addr:
            u = request.user
            u.address = address; u.city = city
            u.postal_code = postal_code; u.country = country
            u.save()

        # Order yarat (unpaid)
        total_local = float(cart_obj.total_price)
        total_pp    = round(total_local * rate, 2)

        order = Order.objects.create(
            user            = request.user,
            total_price     = total_local,
            address         = address,
            city            = city,
            postal_code     = postal_code,
            country         = country,
            note            = note,
            payment_method  = 'paypal',
            status          = 'pending',
        )
        for item in items:
            OrderItem.objects.create(
                order    = order,
                product  = item.product,
                name     = item.product.name,
                price    = item.product.final_price,
                quantity = item.quantity,
            )

        # PayPal order yarat
        base_url   = request.build_absolute_uri('/').rstrip('/')
        return_url = f'{base_url}/checkout/paypal/return/?order_id={order.pk}'
        cancel_url = f'{base_url}/checkout/paypal/cancel/?order_id={order.pk}'

        try:
            pp = create_paypal_order(total_pp, pp_currency, order.pk, return_url, cancel_url)
            order.paypal_order_id = pp['id']
            order.save()
            return redirect(pp['approve_url'])
        except Exception as e:
            order.delete()
            messages.error(request, f'PayPal xətası: {e}')
            return redirect('cart')

    # GET — ünvan formasını göstər (profildən doldur)
    u = request.user
    initial = {
        'address':     u.address,
        'city':        u.city,
        'postal_code': u.postal_code,
        'country':     u.country,
    }
    from .models import Store as StoreModel
    stores = StoreModel.objects.filter(is_active=True)
    return render(request, 'checkout_address.html', {
        'items':    items,
        'cart':     cart_obj,
        'currency': currency,
        'store':    store,
        'stores':   stores,
        'initial':  initial,
    })


@login_required(login_url='/login/')
def checkout_paypal_return(request):
    """PayPal ödənişdən qayıdış — capture et"""
    order_id       = request.GET.get('order_id')
    paypal_token   = request.GET.get('token')          # PayPal order ID
    payer_id       = request.GET.get('PayerID')

    order = get_object_or_404(Order, pk=order_id, user=request.user)

    if order.is_paid:
        return redirect('checkout_success', pk=order.pk)

    try:
        result = capture_paypal_order(order.paypal_order_id or paypal_token)
        if result.get('status') == 'COMPLETED':
            order.is_paid  = True
            order.status   = 'confirmed'
            order.paid_at  = timezone.now()
            order.save()
            # Səbəti təmizlə
            cart_obj = get_or_create_cart(request)
            cart_obj.items.all().delete()
            messages.success(request, 'Ödəniş uğurla tamamlandı!')
            return redirect('checkout_success', pk=order.pk)
        else:
            messages.error(request, 'Ödəniş tamamlanmadı. Yenidən cəhd edin.')
            return redirect('cart')
    except Exception as e:
        messages.error(request, f'Ödəniş xətası: {e}')
        return redirect('cart')


def checkout_paypal_cancel(request):
    """PayPal ləğv edildi"""
    order_id = request.GET.get('order_id')
    if order_id:
        Order.objects.filter(pk=order_id, is_paid=False).delete()
    messages.warning(request, 'Ödəniş ləğv edildi.')
    return redirect('cart')


@login_required(login_url='/login/')
def checkout_success(request, pk):
    """Uğurlu sifariş səhifəsi"""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'checkout_success.html', {'order': order})