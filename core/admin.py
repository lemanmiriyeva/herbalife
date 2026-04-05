from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Category, Product, Cart, CartItem, User, Order, OrderItem,BlogCategory, BlogPost
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
# ── Category ─────────────────────────────────────────────
@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

from .models import Store, ProductStore
 
class ProductStoreInline(admin.TabularInline):
    model   = ProductStore
    extra   = 3   # AZ, US, CA üçün 3 sətir
    fields  = ('store', 'price', 'discount_price', 'is_active', 'stock')
 
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display  = ('code', 'name', 'currency', 'is_active')
    list_editable = ('is_active',)
 
# ── Product ─────────────────────────────────────────────
@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('name', 'category', 'price', 'badge', 'is_addable', 'is_active', 'stock')
    list_filter = ('category', 'badge', 'is_active', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'stock', 'badge', 'is_addable')
    inlines = [ProductStoreInline]


# ── Cart & CartItem ────────────────────────────────────
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'added_at')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_key', 'total_items', 'total_price', 'created_at')
    readonly_fields = ('session_key',)
    inlines = [CartItemInline]

    def total_items(self, obj):
        return obj.total_items

    def total_price(self, obj):
        return f'${obj.total_price}'


# ── Custom User ────────────────────────────────────────
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model  = User
        fields = ('phone', 'email', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model  = User
        fields = ('phone', 'email', 'first_name', 'last_name',
                  'is_active', 'is_staff', 'is_superuser',
                  'groups', 'user_permissions')

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'phone', 'email', 'first_name', 'last_name', 'is_staff')
    
    # Phone sahəsini add/change formlarına əlavə et
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone', 'email', 'password1', 'password2'),
        }),
    )
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Əlaqə', {'fields': ('phone',)}),
    )

# ── Order ─────────────────────────────────────────────
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'name', 'price', 'quantity')


@admin.register(Order)
class OrderAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display   = ('id', 'customer_phone', 'status', 'total_price', 'created_at')
    list_filter    = ('status',)
    readonly_fields = ('created_at',)
    inlines        = [OrderItemInline]

    def customer_phone(self, obj):
        return obj.customer_phone
    customer_phone.short_description = 'Müştəri nömrəsi'


@admin.register(BlogCategory)
class BlogCategoryAdmin(TranslationAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
 
@admin.register(BlogPost)
class BlogPostAdmin(TranslationAdmin):
    list_display  = ('title', 'category', 'author', 'is_featured', 'is_published', 'published_at')
    list_filter   = ('category', 'is_featured', 'is_published')
    search_fields = ('title', 'body', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured', 'is_published')
    raw_id_fields = ('author',)
    fieldsets = (
        (None, {'fields': ('category', 'author', 'title', 'slug')}),
        ('Content', {'fields': ('excerpt', 'body', 'cover_image', 'cover_emoji')}),
        ('Settings', {'fields': ('read_time', 'is_featured', 'is_published', 'published_at')}),
    )
 
from .models import Wishlist
 
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display  = ('user', 'product', 'added_at')
    list_filter   = ('added_at',)
    search_fields = ('user__phone', 'product__name')
    raw_id_fields = ('user', 'product')