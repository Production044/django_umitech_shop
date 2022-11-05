from django.views.generic import TemplateView, DetailView, ListView
from django.db.models import Max, Avg
from django.shortcuts import render

from . models import Product, Size, Color, Brand
from . import selectors


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_context = {
                    'categories': selectors.find_all_categories_selector(),
                    'search_categories': selectors.search_all_categories_selector(),
                    'featured_products': selectors.new_featured_products_selector(),
                    'new_arrivals': selectors.new_arrivals_products_selector()
        }
        context.update(my_context)
        return context


class CatalogueView(ListView):
    template_name = 'category_2.html'
    model = Product
    context_object_name = 'products'
    slug_url_kwarg = 'slug'
    paginate_by = 15

    def get(self, request, *args, **kwargs):
        self.size = Size.objects.get(name=self.request.GET['size']) \
            if self.request.GET.get('size') else None
        self.color = Color.objects.get(name=self.request.GET['color']) \
            if self.request.GET.get('color') else None
        self.brand = Brand.objects.get(name=self.request.GET['brand']) \
            if self.request.GET.get('brand') else None

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        _filter = {
            'categories__slug': self.kwargs.get('slug')
        }
        if self.size:
            _filter['sizes__name'] = self.size.name

        if self.color:
            _filter['color__name'] = self.color.name

        if self.brand:
            _filter['brand__name'] = self.brand.name

        return Product.objects.prefetch_related(
            'images', 'categories'
        ).filter(**_filter).order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        max_price = Product.objects.aggregate(max_price=Max('price'))
        average_price = Product.objects.aggregate(avg_price=Avg('price'))
        context = super().get_context_data(**kwargs)
        products_ids = self.get_queryset().values_list('id', flat=True)

        my_context = {
            'categories': selectors.find_all_categories_selector(),
            'colors': selectors.find_all_colors_selector(products_ids),
            'sizes': selectors.find_all_sizes_selector(products_ids),
            'brands': selectors.find_all_brands_selector(products_ids),
            'max_price': max_price['max_price'],
            'average_price': average_price['avg_price'],

        }
        context.update(my_context)
        return context


class ProductView(DetailView):
    template_name = 'product.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    queryset = Product.objects.prefetch_related(
        'images', 'categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related_products = Product.objects.filter(categories__in=self.object.categories.all())[:5]
        my_context = {
            'categories': selectors.find_all_categories_selector(),
            'related_products': related_products,
        }
        context.update(my_context)
        return context


class FullCatalogueView(TemplateView):
    template_name = 'full-catalogue.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_context = {
            'categories': selectors.find_all_categories_selector(),
            'search_categories': selectors.search_all_categories_selector(),
        }
        context.update(my_context)
        return context