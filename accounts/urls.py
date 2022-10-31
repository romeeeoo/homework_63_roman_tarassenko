from django.urls import path

from accounts.views import LoginView, logout_view, RegisterView, ProfileView, UserChangeView, AccountsListView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('all-accounts/', AccountsListView.as_view(), name="all_accounts"),
    path('account/<int:pk>/', ProfileView.as_view(), name='account'),
    path('account/<int:pk>/change', UserChangeView.as_view(), name='change'),
]