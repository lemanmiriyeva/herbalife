from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Category, Product, ProductColor, ProductSize, ProductVariant,
    Cart, CartItem, User, Order, OrderItem,
    BlogCategory, BlogPost, Store, ProductStore, Wishlist, UserAddress
)


# ── Category ──────────────────────────────────────────────────────
@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display        = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


# ── Store ─────────────────────────────────────────────────────────
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display  = ('code', 'name', 'currency', 'is_active')
    list_editable = ('is_active',)


# ── Product inlines ───────────────────────────────────────────────

class ProductColorInline(TranslationTabularInline):
    """Rəng — adı AZ/EN-də yazılır, hex kodu və şəkil əlavə edilir"""
    model               = ProductColor
    extra               = 1
    fields              = ('name', 'name_az', 'name_en', 'hex_code', 'image', 'sort_order', 'is_active')
    ordering            = ('sort_order', 'pk')
    verbose_name        = 'Rəng'
    verbose_name_plural = 'Rənglər'


class ProductSizeInline(admin.TabularInline):
    """Ölçü — adı, öz qiyməti (boş olarsa məhsulun qiyməti), stok"""
    model               = ProductSize
    extra               = 1
    fields              = ('name', 'price_override', 'stock', 'sort_order', 'is_active')
    ordering            = ('sort_order', 'pk')
    verbose_name        = 'Ölçü'
    verbose_name_plural = 'Ölçülər'


class ProductVariantInline(admin.TabularInline):
    """
    Variant = Rəng + Ölçü kombinasiyası
    Əvvəlcə Rənglər və Ölçülər tab-larında qeydlər yarat,
    sonra burada onları birləşdir.
    """
    model               = ProductVariant
    extra               = 1
    fields              = ('color', 'size', 'price_override', 'stock', 'is_active')
    verbose_name        = 'Variant'
    verbose_name_plural = 'Variantlar (Rəng + Ölçü kombinasiyaları)'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Yalnız həmin məhsulun rəng/ölçülərini göstər"""
        product_id = request.resolver_match.kwargs.get('object_id')
        if product_id:
            if db_field.name == 'color':
                kwargs['queryset'] = ProductColor.objects.filter(
                    product_id=product_id, is_active=True
                ).order_by('sort_order')
            if db_field.name == 'size':
                kwargs['queryset'] = ProductSize.objects.filter(
                    product_id=product_id, is_active=True
                ).order_by('sort_order')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductStoreInline(admin.TabularInline):
    model  = ProductStore
    extra  = 3
    fields = ('store', 'price', 'discount_price', 'is_active', 'stock')


# ── Product ───────────────────────────────────────────────────────
@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display  = ('name', 'category', 'price', 'badge', 'is_addable',
                     'is_active', 'color_count', 'size_count', 'variant_count')
    list_filter   = ('category', 'badge', 'is_active', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'badge', 'is_addable')
    inlines       = [ProductColorInline, ProductSizeInline, ProductVariantInline, ProductStoreInline]

    fieldsets = (
        ('Əsas məlumat', {
            'fields': ('category', 'name', 'slug', 'badge', 'description', 'image')
        }),
        ('Qiymət və Stok', {
            'fields': ('price', 'discount_price', 'price_note', 'stock', 'is_addable', 'is_active', 'is_featured')
        }),
    )

    def color_count(self, obj):
        n = obj.colors.filter(is_active=True).count()
        return f'{n} rəng' if n else '—'
    color_count.short_description = 'Rənglər'

    def size_count(self, obj):
        n = obj.sizes.filter(is_active=True).count()
        return f'{n} ölçü' if n else '—'
    size_count.short_description = 'Ölçülər'

    def variant_count(self, obj):
        n = obj.variants.filter(is_active=True).count()
        return f'{n} variant' if n else '—'
    variant_count.short_description = 'Variantlar'


# ── Cart ──────────────────────────────────────────────────────────
class CartItemInline(admin.TabularInline):
    model           = CartItem
    extra           = 0
    readonly_fields = ('product', 'variant', 'quantity', 'added_at')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display    = ('id', 'session_key', 'total_items', 'total_price', 'created_at')
    readonly_fields = ('session_key',)
    inlines         = [CartItemInline]

    def total_items(self, obj): return obj.total_items
    def total_price(self, obj): return f'{obj.total_price:.2f}'


# ── User ──────────────────────────────────────────────────────────
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ('username', 'phone', 'email', 'first_name', 'last_name', 'is_staff')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone', 'email', 'password1', 'password2'),
        }),
    )
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Əlaqə', {'fields': ('phone',)}),
    )


# ── Order ─────────────────────────────────────────────────────────
class OrderItemInline(admin.TabularInline):
    model           = OrderItem
    extra           = 0
    readonly_fields = ('product', 'name', 'price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = ('id', 'customer_phone', 'status', 'total_price', 'created_at')
    list_filter     = ('status',)
    readonly_fields = ('created_at',)
    inlines         = [OrderItemInline]

    def customer_phone(self, obj): return obj.customer_phone
    customer_phone.short_description = 'Müştəri'


# ── Blog ──────────────────────────────────────────────────────────
@admin.register(BlogCategory)
class BlogCategoryAdmin(TranslationAdmin):
    list_display        = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(TranslationAdmin):
    list_display        = ('title', 'category', 'author', 'is_featured', 'is_published', 'published_at')
    list_filter         = ('category', 'is_featured', 'is_published')
    search_fields       = ('title', 'body', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    list_editable       = ('is_featured', 'is_published')
    raw_id_fields       = ('author',)


# ── Wishlist ──────────────────────────────────────────────────────
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display  = ('user', 'product', 'added_at')
    search_fields = ('user__phone', 'product__name')
    raw_id_fields = ('user', 'product')
