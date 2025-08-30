from django.shortcuts import render, redirect, get_object_or_404
from .models import LoanProduct, Loan
from .forms import LoanProductForm, LoanForm


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



def loan_list(request):
    loans = Loan.objects.select_related('member', 'product').order_by('-disbursed_on')
    return render(request, "loans/loan_list.html", {"loans": loans})

def loan_create(request):
    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("loan_list")
    else:
        form = LoanForm()
    return render(request, "loans/loan_form.html", {"form": form})

def loan_detail(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    return render(request, "loans/loan_detail.html", {"loan": loan})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Loan
from .forms import LoanForm

# Existing views: loan_list, loan_create, loan_detail

def loan_update(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == "POST":
        form = LoanForm(request.POST, instance=loan)
        if form.is_valid():
            form.save()
            return redirect("loan_list")
    else:
        form = LoanForm(instance=loan)
    return render(request, "loans/loan_form.html", {"form": form, "loan": loan, "is_edit": True})

def loan_delete(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == "POST":
        loan.delete()
        return redirect("loan_list")
    return render(request, "loans/loan_confirm_delete.html", {"loan": loan})
