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


# loans/views.py
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from .models import LoanSchedule, Loan
from .forms import LoanScheduleForm

class LoanScheduleListView(ListView):
    model = LoanSchedule
    template_name = "loans/loanschedule_list.html"
    context_object_name = "schedules"

    def get_queryset(self):
        # Optional: support filtering by loan with ?loan=<id>
        qs = super().get_queryset().select_related("loan", "loan__member", "loan__product")
        loan_id = self.request.GET.get("loan")
        if loan_id:
            qs = qs.filter(loan_id=loan_id)
        return qs


class LoanScheduleCreateView(CreateView):
    model = LoanSchedule
    form_class = LoanScheduleForm
    template_name = "loans/loanschedule_form.html"

    def get_success_url(self):
        # Redirect back to list filtered by this loan for convenience
        return f"{reverse('loanschedule_list')}?loan={self.object.loan_id}"


class LoanScheduleUpdateView(UpdateView):
    model = LoanSchedule
    form_class = LoanScheduleForm
    template_name = "loans/loanschedule_form.html"

    def get_success_url(self):
        return f"{reverse('loanschedule_list')}?loan={self.object.loan_id}"


class LoanScheduleDeleteView(DeleteView):
    model = LoanSchedule
    template_name = "loans/confirm_delete.html"

    def get_success_url(self):
        return f"{reverse('loanschedule_list')}?loan={self.object.loan_id}"


# Optional nested create under a loan: /loans/<loan_id>/schedules/add/
class LoanScheduleCreateForLoanView(CreateView):
    model = LoanSchedule
    form_class = LoanScheduleForm
    template_name = "loans/loanschedule_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.loan = get_object_or_404(Loan, pk=kwargs["loan_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial["loan"] = self.loan
        # Suggest next installment number
        last = self.loan.schedule.order_by("-installment_no").first()
        initial["installment_no"] = (last.installment_no + 1) if last else 1
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Fix loan field to this loan, non-editable
        form.fields["loan"].initial = self.loan
        form.fields["loan"].disabled = True
        return form

    def form_valid(self, form):
        form.instance.loan = self.loan
        return super().form_valid(form)

    def get_success_url(self):
        return f"{reverse('loanschedule_list')}?loan={self.loan.id}"
