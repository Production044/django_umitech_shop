from .models import Product, Category, Size, Brand, Color
from django.db.models import Count, QuerySet


def new_arrivals_products_selector(products_limit: int = 5):
    return Product.objects.prefetch_related(
        'images', 'categories'
    ).order_by('-date_created')[:products_limit]


def new_featured_products_selector(products_limit: int = 10):
    return Product.objects.prefetch_related(
        'images', 'categories'
    ).order_by('?')[:products_limit]


def find_all_categories_selector(category_limit: int = 15):
    return Category.objects.all()[:category_limit]


def search_all_categories_selector():
    return Category.objects.prefetch_related(
        'products'
    ).annotate(
        product_count=Count('products')
    ).filter(
        product_count__gte=10
    ).order_by('-product_count')


def find_all_sizes_selector(products_ids: list[int]) -> QuerySet[Size]:
    return Size.objects.filter(
        products__id__in=products_ids
    ).distinct().order_by('name')


def find_all_brands_selector(products_ids: list[int]) -> QuerySet[Brand]:
    return Brand.objects.filter(
        products__id__in=products_ids
    ).distinct().order_by('name')


def find_all_colors_selector(products_ids: list[int]) -> QuerySet[Brand]:
    return Color.objects.filter(
        products__id__in=products_ids
    ).distinct().order_by('name')



