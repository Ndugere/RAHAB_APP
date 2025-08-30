from django.shortcuts import render, redirect, get_object_or_404
from .models import LoanProduct
from .forms import LoanProductForm

def loanproduct_list(request):
    products = LoanProduct.objects.all().order_by("name")
    return render(request, "loans/loanproduct_list.html", {"products": products})

def loanproduct_create(request):
    if request.method == "POST":
        form = LoanProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("loanproduct_list")
    else:
        form = LoanProductForm()
    return render(request, "loans/loanproduct_form.html", {"form": form})


def loanproduct_edit(request, pk):
    product = get_object_or_404(LoanProduct, pk=pk)
    if request.method == "POST":
        form = LoanProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("loanproduct_list")
    else:
        form = LoanProductForm(instance=product)
    return render(request, "loans/loanproduct_form.html", {"form": form, "product": product})


def loanproduct_delete(request, pk):
    product = get_object_or_404(LoanProduct, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("loanproduct_list")
    return render(request, "loans/loanproduct_confirm_delete.html", {"product": product})
