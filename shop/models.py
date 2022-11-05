from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=35)
    name_en = models.CharField(max_length=35, default='')
    slug = models.SlugField(unique=True)


    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(
        'shop.Product', on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='images', null=True)
    base_url = models.URLField()

    def __str__(self):
        return self.image.url


class Product(models.Model):
    base_url = models.URLField()
    title = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255, default='')
    slug = models.SlugField(max_length=255, unique=True)
    description = models.CharField(max_length=5000, default='')
    description_en = models.CharField(max_length=5000, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default='')
    discount = models.CharField(max_length=80, default='')
    # old_price = models.DecimalField(max_digits=10, decimal_places=2, default='')
    availability = models.BooleanField(default=False)
    availability_in = models.CharField(max_length=80, default='')
    date_created = models.DateTimeField(auto_now_add=True)

    categories = models.ManyToManyField(Category, related_name='products')
    sizes = models.ManyToManyField(Size, blank=True, default='', related_name='products')
    color = models.ForeignKey(
        Color, related_name='products', on_delete=models.SET_NULL,
        blank=True, null=True
    )
    brand = models.ForeignKey(
        Brand, related_name='products', on_delete=models.SET_NULL,
        null=True, blank=True, default=''
    )

    def __str__(self):
        return self.title


