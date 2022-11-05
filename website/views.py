from django.views.generic import FormView, TemplateView, ListView
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse

from shop import selectors
from shop.models import Product
from utils.email import send_html_email
from . forms import ContactForm
from .models import Contact


class ContactView(FormView):
    template_name = 'contact.html'
    model = Contact
    form_class = ContactForm
    success_url = '/contact/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_context = {
                    'categories': selectors.find_all_categories_selector(),
        }
        context.update(my_context)
        return context

    def form_valid(self, form):
        Contact.objects.create(**form.cleaned_data)
        to_email = form.cleaned_data.get('email')
        send_html_email(
            subject='Раді бачити нового користувача!',
            to_email=[to_email],
            context={
                'name': form.cleaned_data.get('name'),
                'link': self.request.build_absolute_uri(reverse('index')),
            },
            template_name='email/email.html'
        )
        messages.add_message(
            self.request, messages.SUCCESS,
            'Дякую за ваше повідомлення!'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.WARNING,
            'Ви допустили помилку!'
        )
        return super().form_invalid(form)

# class InfoView(TemplateView):
#     template_name = ''


class SearchView(ListView):
    template_name = 'category_2.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 9

    def get(self, request, *args, **kwargs):
        self.search_query = self.request.GET.get('search')
        print(self.search_query)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        _filter = None
        _filter = Q(title__icontains=self.search_query) | Q(description__icontains=self.search_query)  # searchVector in progress
        return Product.objects.prefetch_related(
            'images', 'categories'
        ).filter(_filter).order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        my_context = {
            'search_query': self.search_query,
            'search_result_count': self.get_queryset().count(),
            'categories': selectors.find_all_categories_selector(),
        }
        context.update(my_context)
        return context