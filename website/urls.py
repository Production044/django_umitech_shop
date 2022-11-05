from django.urls import path


from . import views


urlpatterns = [
    path('search/', views.SearchView.as_view(), name='search'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]