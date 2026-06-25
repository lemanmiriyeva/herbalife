from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Product, ProductColor, User, Order, OrderItem, BlogCategory, BlogPost


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Category, CategoryTranslationOptions)


class ProductTranslationOptions(TranslationOptions):
    # badge artıq 'new'/'bestseller' key-dir — API BADGE_LABELS ilə çevirir
    # flavor_name/flavor_color köhnə legacy sahədir — translation lazım deyil
    fields = ('name', 'description', 'price_note')

translator.register(Product, ProductTranslationOptions)


class ProductColorTranslationOptions(TranslationOptions):
    # Rəng adı AZ/EN-də fərqli ola bilər (məs. "Şokolad" / "Chocolate")
    fields = ('name',)

translator.register(ProductColor, ProductColorTranslationOptions)


class UserTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name')

translator.register(User, UserTranslationOptions)


class OrderTranslationOptions(TranslationOptions):
    fields = ('note',)

translator.register(Order, OrderTranslationOptions)


class OrderItemTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(OrderItem, OrderItemTranslationOptions)


class BlogCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(BlogCategory, BlogCategoryTranslationOptions)


class BlogPostTranslationOptions(TranslationOptions):
    fields = ('title', 'excerpt', 'body')

translator.register(BlogPost, BlogPostTranslationOptions)
