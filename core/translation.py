# core/translation.py
from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Product, User, Order, OrderItem,BlogCategory, BlogPost
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Category, CategoryTranslationOptions)


class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'price_note', 'flavor_name', 'flavor_color', 'badge')

translator.register(Product, ProductTranslationOptions)


class UserTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name')

translator.register(User, UserTranslationOptions)


class OrderTranslationOptions(TranslationOptions):
    fields = ('note',)  # status choices-dır, note isə sərbəst mətn

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