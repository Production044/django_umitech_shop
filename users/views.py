from django.views.generic import FormView
from django.contrib.auth import get_user_model
from .forms import SignUpForm

User = get_user_model()


class SignUpView(FormView):
    template_name = 'login_register.html'
    model = User
    form_class = SignUpForm
    success_url = 'signup/'

    def form_valid(self, form):
        print(form.cleaned_data)

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
