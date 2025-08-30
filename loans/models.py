from django.db import models
from django.utils import timezone
from core.models import Member, Account, JournalEntry, ReportTag


from django.db import models

class LoanProduct(models.Model):
    """Defines a loan type with default terms."""
    REDUCING = "REDUCING"
    FLAT = "FLAT"
    INTEREST_METHODS = [
        (REDUCING, "Reducing balance"),
        (FLAT, "Flat"),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    annual_rate = models.DecimalField(max_digits=5, decimal_places=2)  # %
    interest_method = models.CharField(
        max_length=16,
        choices=INTEREST_METHODS
        # No default — forces user to choose
    )
    default_tenor_months = models.PositiveIntegerField()

    def __str__(self):
        return self.name



class Loan(models.Model):
    """A loan issued to a member."""
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    DEFAULTED = "DEFAULTED"
    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (CLOSED, "Closed"),
        (DEFAULTED, "Defaulted"),
    ]

    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    product = models.ForeignKey(LoanProduct, on_delete=models.PROTECT)
    principal = models.DecimalField(max_digits=14, decimal_places=2)
    annual_rate = models.DecimalField(max_digits=5, decimal_places=2)
    interest_method = models.CharField(max_length=16, choices=LoanProduct.INTEREST_METHODS)
    disbursed_on = models.DateField()
    tenor_months = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)

    # Accounting integration
    principal_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="loan_principal_account",
        limit_choices_to={"report_tag": ReportTag.ASSET_LOANS_PRINCIPAL}
    )
    interest_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="loan_interest_account",
        limit_choices_to={"report_tag": ReportTag.ASSET_LOAN_INTEREST}
    )

    def __str__(self):
        return f"Loan #{self.id} - {self.member.full_name}"


class LoanSchedule(models.Model):
    """Planned repayment installments for a loan."""
    loan = models.ForeignKey(Loan, related_name="schedule", on_delete=models.CASCADE)
    installment_no = models.PositiveIntegerField()
    due_date = models.DateField()
    principal_due = models.DecimalField(max_digits=14, decimal_places=2)
    interest_due = models.DecimalField(max_digits=14, decimal_places=2)
    total_due = models.DecimalField(max_digits=14, decimal_places=2)
    paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ("loan", "installment_no")
        ordering = ["due_date"]

    def __str__(self):
        return f"Loan {self.loan.id} - Installment {self.installment_no}"


class LoanRepayment(models.Model):
    """Actual payments made towards a loan."""
    loan = models.ForeignKey(Loan, related_name="repayments", on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    principal_component = models.DecimalField(max_digits=14, decimal_places=2)
    interest_component = models.DecimalField(max_digits=14, decimal_places=2)
    journal_entry = models.ForeignKey(JournalEntry, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Repayment for Loan {self.loan.id} on {self.date}"


