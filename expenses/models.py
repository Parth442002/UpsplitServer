from django.core.exceptions import ValidationError
from django.db import models

from django.contrib.auth import get_user_model
import uuid
user_model = get_user_model()

# Create your models here.


class Borrower(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    amount_borrowed = models.DecimalField(max_digits=8, decimal_places=2)
    amount_repayed = models.DecimalField(max_digits=8, decimal_places=2)


class Expense(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    lender = models.ForeignKey(
        user_model, on_delete=models.CASCADE, related_name='expenses_lent')
    borrowers = models.ManyToManyField(
        Borrower, related_name='expenses_borrowed', blank=True, null=True)
    amount_borrowed = models.DecimalField(max_digits=8, decimal_places=2)
    amount_repayed = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    @property
    def borrower_details(self):
        borrower_details = {}
        for borrower in self.borrowers.all():
            borrower_details[borrower.user.username] = {
                'amount_borrowed': borrower.amount_borrowed,
                'amount_repayed': borrower.amount_repayed,
            }
        return borrower_details
