from django.urls import path
from receipts import views
from receipts.views import ReceiptPrintView

app_name = "receipts"

urlpatterns = [
    path("receipts/", views.receipt_list, name="receipt_list"),
    path("receipts/<int:pk>/", views.receipt_detail, name="receipt_detail"),

    # Print-friendly receipt view
    path("receipts/<int:pk>/print/", ReceiptPrintView.as_view(), name="receipt_print"),
]
