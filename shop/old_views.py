from random import sample

from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Max
from django.views.generic import TemplateView, DetailView, ListView

from . models import Product, Image, Category, Size
from . import selectors

# def index(request):
#     categories = Category.objects.all()[:10]
#     search_categories = Category.objects.prefetch_related(
#         'products'
#     ).annotate(
#         product_count=Count('products')
#     ).filter(
#         product_count__gte=10
#     ).order_by('-product_count')
#     products = Product.objects.prefetch_related('images', 'categories').order_by('?')[:10]
#
#     new_arrivals = Product.objects.prefetch_related('images', 'categories').order_by('-date_created')[:5]
#
#     context = {
#         # 'categories': search_categories[:10],
#         'categories': categories,
#         'search_categories': search_categories,
#         'featured_products': products,
#         'new_arrivals': new_arrivals
#     }
#     return render(request, 'index.html', context)


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


# def catalogue(request, **kwargs):
#     categories = Category.objects.all()[:10]
#     category = get_object_or_404(Category, slug=kwargs.get('slug'))
#     products = Product.objects.prefetch_related(
#         'images').filter(categories=category)[:9]
#     # sizes = Size.objects.filter(products__in=products)
#
#     max_price = Product.objects.aggregate(max_price=Max('price'))
#     context = {
#         'products': products,
#         'categories': categories,
#         'max_price': max_price['max_price']
#         # 'size': sizes,
#     }
#     return render(request, 'category_2.html', context)


class CatalogueView(ListView):
    template_name = 'category_2.html'
    model = Product
    context_object_name = 'products'
    slug_url_kwarg = 'slug'
    paginate_by = 9

    def get_queryset(self):
        _filter = {
            'categories__slug': self.kwargs.get('slug')
        }
        return Product.objects.prefetch_related(
            'images', 'categories'
        ).filter(**_filter)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        my_context = {
            'categories': selectors.find_all_categories_selector(),
        }
        context.update(my_context)
        return context


# def product(request, **kwargs):
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

    # categories = Category.objects.all()[:10]
    # item = get_object_or_404(
    #     Product.objects.prefetch_related('images'),
    #     slug=kwargs.get('slug')
    # )
    # related_products = Product.objects.filter(
    #     categories__id__in=item.categories.all()
    # ).values_list('id', flat=True)
    # random_ids = sample(list(related_products), 1)
    # related_products = Product.objects.prefetch_related(
    #     'images', 'categories'
    # ).filter(pk__in=random_ids)
    #
    # context = {
    #     'product': item,
    #     'categories': categories,
    #     'related_products': selectors.new_related_product_selector,
    # }
    # return render(request, 'product.html', context)


def contact(request):
    categories = Category.objects.all()[:10]
    context = {
        'categories': categories,
    }
    return render(request, 'contact.html', context)

# class ContactView(TemplateView):
#     template_name = 'contact.html'

# class InfoView(TemplateView):
#     template_name = ''




#цвет

# <!--                    <div class="sidebar">-->
# <!--                        <h3 class="title">КОЛІР</h3>-->
#
# <!--                        <ul class="sidebar-list">-->
# <!--                            {% for color in colors %}-->
# <!--                            <li><a href="{{request.path}?color={{ color.name }}">-->
# <!--                                <span class="color" style="background-color: "></span> {{ color.name }}</a></li>-->
# <!--                            </li>-->
# <!--                            {% endfor %}-->
#
# <!--                        </ul>-->
# <!--                    </div>-->