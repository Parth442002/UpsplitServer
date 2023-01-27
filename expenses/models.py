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
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    desc = models.TextField(max_length=300, blank=True, null=True)

    lender = models.ForeignKey(
        user_model, on_delete=models.CASCADE, related_name='expenses_lent')
    borrowers = models.ManyToManyField(
        Borrower, related_name='expenses_borrowed')

    totalexpense = models.DecimalField(max_digits=8, decimal_places=2)
    lenders_share = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    totalborrowed = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    totalrepayed = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    is_settled = models.BooleanField(default=False)
