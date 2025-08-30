from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.loanproduct_list, name="loanproduct_list"),
    path("products/new/", views.loanproduct_create, name="loanproduct_create"),
    path("<int:pk>/edit/", views.loanproduct_edit, name="loanproduct_edit"),
    path("<int:pk>/delete/", views.loanproduct_delete, name="loanproduct_delete"),
]
