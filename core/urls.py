from django.urls import path
from . import views, api
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # ── Pages ───────────────────────────────────────────────────
    path('',                            views.home,                    name='home'),
    path('products',                    views.products,                name='products'),
    path('products/<slug:slug>/',       views.product_detail,          name='product_detail'),
    path('cart',                        views.cart,                    name='cart'),
    path('blogs/',                      views.blog,                    name='blog'),
    path('blog/<slug:slug>/',           views.blog_detail,             name='blog_detail'),

    # ── Auth ────────────────────────────────────────────────────
    path('register/',                   views.register_view,           name='register'),
    path('login/',                      views.login_view,              name='login'),
    path('logout/',                     views.logout_view,             name='logout'),

    # ── Profile & Wishlist ──────────────────────────────────────
    path('profile/',                    views.profile_view,            name='profile'),
    path('wishlist/toggle/',            views.wishlist_toggle,         name='wishlist_toggle'),
    path('wishlist/status/',            views.wishlist_status,         name='wishlist_status'),

    # ── Checkout ────────────────────────────────────────────────
    path('checkout/',                   views.checkout_address,        name='checkout'),
    path('checkout/paypal/return/',     views.checkout_paypal_return,  name='checkout_paypal_return'),
    path('checkout/paypal/cancel/',     views.checkout_paypal_cancel,  name='checkout_paypal_cancel'),
    path('checkout/success/<int:pk>/',  views.checkout_success,        name='checkout_success'),

    # ── API ─────────────────────────────────────────────────────
    path('api/filters/',                api.filters,                   name='api_filters'),
    path('api/categories/',             api.categories,                name='api_categories'),
    path('api/products/',               api.products,                  name='api_products'),
    path('api/products/<slug:slug>/',   api.product_detail,            name='api_product_detail'),
    path('api/search/suggest/',         api.search_suggest,            name='api_search_suggest'),
    path('api/cart/',                   api.cart_get,                  name='api_cart'),
    path('api/cart/add/',               api.cart_add,                  name='api_cart_add'),
    path('api/cart/items/<int:item_id>/',        api.cart_update,      name='api_cart_update'),
    path('api/cart/items/<int:item_id>/delete/', api.cart_remove,      name='api_cart_remove'),
    path('api/auth/status/',            api.auth_status,               name='api_auth_status'),
    path('api/blog/posts/',             api.api_blog_posts,            name='api_blog_posts'),
    path('api/blog/posts/<slug:slug>/', api.api_blog_post_detail,      name='api_blog_post_detail'),
    path('api/blog/categories/',        api.api_blog_categories,       name='api_blog_categories'),
    path('api/store/',                  api.store_info,                name='api_store_info'),
    path('api/store/switch/',           csrf_exempt(api.store_switch), name='api_store_switch'),
]