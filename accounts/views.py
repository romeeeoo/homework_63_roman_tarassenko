from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode

from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView, FormView

from accounts.forms import LoginForm, CustomUserCreationForm, UserChangeForm, InstaSearchForm
from accounts.models import Account


class LoginView(TemplateView):
    template_name = 'login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        next = request.GET.get('next')
        form_data = {} if not next else {'next': next}
        form = self.form(form_data)
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            return redirect('login')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        next = form.cleaned_data.get('next')
        user = authenticate(request, email=email, password=password)
        if not user:
            return redirect('login')
        login(request, user)
        if next:
            return redirect(next)
        return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('index')


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = "/"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        context = {}
        context["form"] = form
        return self.render_to_response(context)


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "user_detail.html"
    context_object_name = "user_obj"

    def get_context_data(self, **kwargs):
        posts = self.object.posts.all()
        kwargs["posts"] = posts
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        account_id = int(request.POST.get("pk"))
        print(account_id)
        user = request.user
        Account.subscriptions.create(to_account=account_id, from_account=user)
        return redirect('index')


class UserChangeView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = "user_change.html"
    context_object_name = "user_obj"

    def get_success_url(self):
        return reverse("account", kwargs={"pk": self.object.pk})


class AccountsListView(ListView):
    template_name = "list_accounts.html"
    model = Account
    context_object_name = "accounts"

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            q_username = Account.objects.filter(username__icontains=self.search_value)
            q_email = Account.objects.filter(email__icontains=self.search_value)
            q_first_name = Account.objects.filter(first_name__icontains=self.search_value)
            q_last_name = Account.objects.filter(last_name__icontains=self.search_value)
            queryset = (q_username | q_last_name | q_first_name | q_email).distinct()
        return queryset

    def get_search_form(self):
        return InstaSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

