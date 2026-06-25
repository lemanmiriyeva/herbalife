from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name       = models.CharField(max_length=200, verbose_name=_('Name'))
    slug       = models.SlugField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    BADGE_CHOICES = [
        ('',            _('—')),
        ('new',         _('Yeni')),
        ('bestseller',  _('Çox Satılan')),
    ]

    category       = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name=_('Category'))
    name           = models.CharField(max_length=300, verbose_name=_('Name'))
    slug           = models.SlugField(max_length=300, unique=True, blank=True)
    badge          = models.CharField(max_length=20, choices=BADGE_CHOICES, blank=True, verbose_name=_('Badge'))
    description    = models.TextField(blank=True, verbose_name=_('Description'))
    price          = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('Discount price'))
    price_note     = models.CharField(max_length=50, blank=True, verbose_name=_('Price note'))
    is_addable     = models.BooleanField(default=True, verbose_name=_('Add to cart'))
    image          = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name=_('Image'))
    stock          = models.PositiveIntegerField(default=100, verbose_name=_('Stock'))
    is_active      = models.BooleanField(default=True, verbose_name=_('Active'))
    is_featured    = models.BooleanField(default=False, verbose_name=_('Featured'))
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    # Köhnə sahələr — silinmədi, data itkisi olmasın
    size         = models.CharField(max_length=100, blank=True, verbose_name=_('Size (legacy)'))
    flavor_name  = models.CharField(max_length=100, blank=True, verbose_name=_('Flavor (legacy)'))
    flavor_color = models.CharField(max_length=20,  blank=True, verbose_name=_('Flavor color (legacy)'))

    class Meta:
        verbose_name        = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug, n = base, 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'; n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        return float(self.discount_price) if self.discount_price else float(self.price)

    def get_badge_label(self):
        """Aktiv dildə badge mətnini qaytarır"""
        mapping = {
            'new':        str(_('Yeni')),
            'bestseller': str(_('Çox Satılan')),
        }
        return mapping.get(self.badge, '')


class ProductColor(models.Model):
    """Məhsulun rəng variantı"""
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors', verbose_name=_('Product'))
    name       = models.CharField(max_length=100, verbose_name=_('Color name'))
    hex_code   = models.CharField(max_length=20, blank=True, verbose_name=_('Hex code'), help_text='Məs: #FF5733')
    image      = models.ImageField(upload_to='products/colors/', blank=True, null=True, verbose_name=_('Image'))
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name=_('Sort order'))
    is_active  = models.BooleanField(default=True, verbose_name=_('Active'))

    class Meta:
        verbose_name        = _('Product Color')
        verbose_name_plural = _('Product Colors')
        ordering = ['sort_order', 'pk']

    def __str__(self):
        return f'{self.product.name} — {self.name}'


class ProductSize(models.Model):
    """Məhsulun ölçü variantı"""
    product        = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes', verbose_name=_('Product'))
    name           = models.CharField(max_length=100, verbose_name=_('Size name'), help_text='Məs: 550q, 1kq, S, M, L')
    price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         verbose_name=_('Price override'),
                                         help_text=_('Leave empty to use base product price'))
    stock          = models.PositiveIntegerField(default=100, verbose_name=_('Stock'))
    sort_order     = models.PositiveSmallIntegerField(default=0, verbose_name=_('Sort order'))
    is_active      = models.BooleanField(default=True, verbose_name=_('Active'))

    class Meta:
        verbose_name        = _('Product Size')
        verbose_name_plural = _('Product Sizes')
        ordering = ['sort_order', 'pk']

    def __str__(self):
        return f'{self.product.name} — {self.name}'


class ProductVariant(models.Model):
    """
    Rəng + Ölçü kombinasiyası.
    Admin əlavə edir: məs. Çikolad/550q, Vanil/1kq
    """
    product        = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name=_('Product'))
    color          = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='variants', verbose_name=_('Color'))
    size           = models.ForeignKey(ProductSize, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='variants', verbose_name=_('Size'))
    price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         verbose_name=_('Price override'),
                                         help_text=_('Leave empty to inherit from size or product'))
    stock          = models.PositiveIntegerField(default=100, verbose_name=_('Stock'))
    is_active      = models.BooleanField(default=True, verbose_name=_('Active'))

    class Meta:
        verbose_name        = _('Product Variant')
        verbose_name_plural = _('Product Variants')
        ordering = ['color__sort_order', 'size__sort_order', 'pk']

    def __str__(self):
        parts = [p for p in [
            self.color.name if self.color else None,
            self.size.name  if self.size  else None,
        ] if p]
        return f"{self.product.name} — {' / '.join(parts)}" if parts else f"{self.product.name} (default)"

    @property
    def final_price(self):
        if self.price_override:
            return float(self.price_override)
        if self.size and self.size.price_override:
            return float(self.size.price_override)
        return self.product.final_price

    @property
    def effective_image(self):
        if self.color and self.color.image:
            return self.color.image
        return self.product.image


class Cart(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart #{self.pk}'

    @property
    def total_price(self):
        return sum(i.subtotal for i in self.items.select_related('product', 'variant').all())

    @property
    def total_items(self):
        return sum(i.quantity for i in self.items.all())


class CartItem(models.Model):
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant  = models.ForeignKey('ProductVariant', on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='cart_items', verbose_name=_('Variant'))
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'product', 'variant']

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'

    @property
    def subtotal(self):
        unit = self.variant.final_price if self.variant else self.product.final_price
        return unit * self.quantity


class User(AbstractUser):
    phone       = models.CharField(max_length=20, unique=True, blank=True, verbose_name=_('Phone'))
    address     = models.CharField(max_length=255, blank=True, verbose_name=_('Address'))
    city        = models.CharField(max_length=100, blank=True, verbose_name=_('City'))
    postal_code = models.CharField(max_length=20,  blank=True, verbose_name=_('Postal code'))
    country     = models.CharField(max_length=10,  blank=True, verbose_name=_('Country'),
                                   help_text='Store code: AZ, US, CA')

    class Meta:
        verbose_name        = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',   _('Pending')),
        ('confirmed', _('Confirmed')),
        ('cancelled', _('Cancelled')),
    ]

    user            = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name=_('User'))
    guest_phone     = models.CharField(max_length=20, blank=True, verbose_name=_('Guest phone'))
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('Status'))
    total_price     = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Total'))
    note            = models.TextField(blank=True, verbose_name=_('Note'))
    address         = models.CharField(max_length=255, blank=True, verbose_name=_('Address'))
    city            = models.CharField(max_length=100, blank=True, verbose_name=_('City'))
    postal_code     = models.CharField(max_length=20,  blank=True, verbose_name=_('Postal code'))
    country         = models.CharField(max_length=10,  blank=True, verbose_name=_('Country'))
    payment_method  = models.CharField(max_length=20, default='paypal', verbose_name=_('Payment method'))
    paypal_order_id = models.CharField(max_length=100, blank=True, verbose_name=_('PayPal Order ID'))
    is_paid         = models.BooleanField(default=False, verbose_name=_('Paid'))
    paid_at         = models.DateTimeField(null=True, blank=True, verbose_name=_('Paid at'))
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk}'

    @property
    def customer_phone(self):
        return self.user.phone if self.user else self.guest_phone


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    name     = models.CharField(max_length=300)
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name        = _('Order item')
        verbose_name_plural = _('Order items')

    def __str__(self):
        return f'{self.name} x{self.quantity}'

    @property
    def subtotal(self):
        return float(self.price) * self.quantity


class BlogCategory(models.Model):
    name       = models.CharField(max_length=100, verbose_name=_('Name'))
    slug       = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = _('Blog Category')
        verbose_name_plural = _('Blog Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    category     = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name=_('Category'))
    title        = models.CharField(max_length=300, verbose_name=_('Title'))
    slug         = models.SlugField(max_length=300, unique=True, blank=True)
    excerpt      = models.TextField(blank=True, verbose_name=_('Excerpt'))
    body         = models.TextField(verbose_name=_('Body'))
    cover_image  = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name=_('Cover image'))
    cover_emoji  = models.CharField(max_length=10, blank=True, default='📝', verbose_name=_('Cover emoji'))
    author       = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_posts', verbose_name=_('Author'))
    read_time    = models.PositiveIntegerField(default=5, verbose_name=_('Read time (min)'))
    is_featured  = models.BooleanField(default=False, verbose_name=_('Featured'))
    is_published = models.BooleanField(default=True, verbose_name=_('Published'))
    published_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Published at'))
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = _('Blog Post')
        verbose_name_plural = _('Blog Posts')
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug, n = base, 1
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'; n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_author_name(self):
        if self.author:
            return self.author.get_full_name() or self.author.username
        return 'Herbalife Nutrition'


class Store(models.Model):
    CURRENCY_CHOICES = [
        ('AZN', 'AZN (₼)'),
        ('USD', 'USD ($)'),
        ('CAD', 'CAD (CA$)'),
    ]

    code          = models.CharField(max_length=10, unique=True, verbose_name=_('Code'))
    name          = models.CharField(max_length=100, verbose_name=_('Name'))
    currency      = models.CharField(max_length=10, choices=CURRENCY_CHOICES, verbose_name=_('Currency'))
    is_active     = models.BooleanField(default=True, verbose_name=_('Active'))
    country_codes = models.CharField(max_length=200, blank=True, help_text='Vergüllə ayrılmış ISO ölkə kodları: AZ,US,CA', verbose_name=_('Country codes'))

    class Meta:
        verbose_name        = _('Store')
        verbose_name_plural = _('Stores')

    def __str__(self):
        return f'{self.name} ({self.currency})'


class ProductStore(models.Model):
    product        = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='store_prices')
    store          = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_prices')
    price          = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('Discount price'))
    is_active      = models.BooleanField(default=True, verbose_name=_('Active in this store'))
    stock          = models.PositiveIntegerField(default=100, verbose_name=_('Stock'))

    class Meta:
        unique_together     = ['product', 'store']
        verbose_name        = _('Product Store Price')
        verbose_name_plural = _('Product Store Prices')

    def __str__(self):
        return f'{self.product.name} — {self.store.code}: {self.price}'

    @property
    def final_price(self):
        return float(self.discount_price) if self.discount_price else float(self.price)


class Wishlist(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together     = ['user', 'product']
        verbose_name        = _('Wishlist Item')
        verbose_name_plural = _('Wishlist Items')
        ordering            = ['-added_at']

    def __str__(self):
        return f'{self.user.username} → {self.product.name}'


class UserAddress(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name=_('User'))
    title       = models.CharField(max_length=100, verbose_name=_('Title'), help_text='Ev, İş, Digər')
    address     = models.CharField(max_length=255, verbose_name=_('Address'))
    city        = models.CharField(max_length=100, verbose_name=_('City'))
    postal_code = models.CharField(max_length=20, blank=True, verbose_name=_('Postal code'))
    country     = models.CharField(max_length=10, verbose_name=_('Country'))
    is_default  = models.BooleanField(default=False, verbose_name=_('Default'))
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = _('User Address')
        verbose_name_plural = _('User Addresses')
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f'{self.title} — {self.city}'
