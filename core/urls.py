from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Accounts
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/new/', views.account_create, name='account_create'),
    path('accounts/<int:pk>/edit/', views.account_edit, name='account_edit'),

    # Journal Entries
    path('journal-entries/', views.journal_entry_list, name='journal_entry_list'),
    path('journal-entries/new/', views.journal_entry_create, name='journal_entry_create'),
    path('journal-entries/<int:pk>/edit/', views.journal_entry_edit, name='journal_entry_edit'),
    path('journal-entries/<int:pk>/delete/', views.journal_entry_delete, name='journal_entry_delete'),

    # -----------------------------
    # Member routes
    # -----------------------------
    path("members/", views.member_list, name="member_list"),
    path("members/add/", views.member_create, name="member_create"),
    path("members/<int:pk>/", views.member_detail, name="member_detail"),
    path("members/<int:pk>/edit/", views.member_edit, name="member_edit"),
    path("members/<int:pk>/delete/", views.member_delete, name="member_delete"),
]
