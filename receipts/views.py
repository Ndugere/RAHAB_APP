from django.views.generic import DetailView
from receipts.models import Receipt
from django.shortcuts import render, get_object_or_404
from receipts.models import Receipt


class ReceiptPrintView(DetailView):
    model = Receipt
    template_name = "receipts/receipt_print.html"

def receipt_list(request):
    """
    Displays a list of all receipts, ordered by most recent.
    Supports optional search by member name.
    """
    query = request.GET.get("q", "").strip()
    receipts = Receipt.objects.select_related("member", "issued_by").order_by("-issued_on")

    if query:
        receipts = receipts.filter(member__full_name__icontains=query)

    context = {
        "receipts": receipts,
        "query": query,
    }
    return render(request, "receipts/receipt_list.html", context)


def receipt_detail(request, pk):
    """
    Displays the details of a single receipt.
    """
    receipt = get_object_or_404(Receipt, pk=pk)
    return render(request, "receipts/receipt_detail.html", {"receipt": receipt})
