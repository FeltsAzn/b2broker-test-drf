import decimal
from decimal import Decimal

from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models


class Wallet(models.Model):
    label = models.CharField(max_length=100)
    balance = models.DecimalField(
        max_digits=36,
        decimal_places=18,
        validators=[MinValueValidator(Decimal("0"))],
        default=decimal.Decimal("0.0")
    )

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    txid = models.CharField(max_length=18, unique=True, validators=[MinLengthValidator(18)])
    amount = models.DecimalField(max_digits=36, decimal_places=18)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

        indexes = [
            models.Index(fields=["txid"]),
            models.Index(fields=["wallet"]),
        ]
