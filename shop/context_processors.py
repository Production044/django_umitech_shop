# from django.db.models import Count
#
# from .models import Category
#
#
# def categories_menu(request):
#     categories = Category.objects.prefetch_related(
#         'products'
#     ).annotate(
#         product_count=Count('products')
#     ).order_by('-product_count')
#     return {
#         'search_categories': categories,
#     }