from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django_summernote.admin import SummernoteModelAdmin

from .actions import translate_product, translate_name
from . models import Category, Color, Product, Image, Size, Brand


class ImageInlineAdmin(admin.StackedInline):
    model = Image
    fields = ('picture', 'image')
    readonly_fields = fields
    extra = 0

    @staticmethod
    def picture(obj):
        return format_html(
            '<img src="{}" style="max-width: 70px">', obj.image.url
          )


class ProductAdmin(SummernoteModelAdmin):
    actions = (translate_product,)
    summernote_fields = ('description', 'description_en')
    inlines = (ImageInlineAdmin,)
    list_display = ('title', 'translated', 'price', 'brand', 'availability')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',) # пошук по фільтрам не працює
    # list_filter = ('color', 'brand')
    list_editable = ('availability',)

    fieldsets = (
        (None, {
            'fields': (
                'base_url', 'slug',
                ('title', 'title_en',),
                ('description',),
                ('description_en',),
                ('price', 'discount', 'availability', 'availability_in'),
                ('categories', 'sizes'),
                ('color', 'brand')

            )
        }),
    )

    @staticmethod
    def translated(obj):
        if obj.title_en and obj.description_en:
            return mark_safe('<img src="/static/admin/img/icon-yes.svg" alt=True>')
        return mark_safe('<img src="/static/admin/img/icon-no.svg" alt=False>')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('picture',)

    @staticmethod
    def picture(obj):
        return format_html(
            '<img src="{}" style="max-width: 100px">', obj.image.url
          )


#------------------------[Сортування в адмін панелі]----------------------------

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_products')
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('products')

    @staticmethod
    def total_products(obj):
        count = obj.products.count()
        link = f'/admin/shop/product/?brand__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} products </a>')


class ColorAdmin(admin.ModelAdmin):
    actions = (translate_name,)
    list_display = ('name', 'name_en', 'total_products')
    search_fields = ('name', 'name_en')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('products')

    @staticmethod
    def total_products(obj):
        count = obj.products.count()
        link = f'/admin/shop/product/?color__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} products </a>')


class CategoryAdmin(admin.ModelAdmin):
    actions = (translate_name,)
    list_display = ('name', 'name_en', 'total_products', 'slug')
    search_fields = ('name', 'name_en')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('products')

    @staticmethod
    def total_products(obj):
        count = obj.products.count()
        link = f'/admin/shop/product/?categories__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} products </a>')


class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_products')
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('products')

    @staticmethod
    def total_products(obj):
        count = obj.products.count()
        link = f'/admin/shop/product/?sizes__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} products </a>')

#------------------------[Кінець сортування в адмін панелі]----------------------------


admin.site.register(Category, CategoryAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Brand, BrandAdmin)
