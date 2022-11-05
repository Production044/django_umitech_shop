from shop.models import Category


def find_all_categories_selector(category_limit: int = 10):
    return Category.objects.all()[:category_limit]