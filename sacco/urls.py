from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from core.views import MyLoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('accounts/login/', MyLoginView.as_view(), name='login'),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(next_page=reverse_lazy('login')),
        name='logout'
    ),

    # Password reset flow
    path(
        'accounts/password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='core/password_reset_form.html'
        ),
        name='password_reset'
    ),
    path(
        'accounts/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='core/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'accounts/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='core/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'accounts/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='core/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # App URLs
    path('', include('core.urls')),
]
