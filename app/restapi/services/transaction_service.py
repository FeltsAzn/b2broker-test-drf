import decimal

from django.db import transaction
from rest_framework import serializers

from restapi.models import Transaction, Wallet


class TransactionService:
    @staticmethod
    @transaction.atomic
    def perform_transaction(wallet: Wallet, txid: str, amount: decimal.Decimal) -> Transaction:
        if wallet.balance + amount < 0:
            raise serializers.ValidationError("Transaction could not be completed, insufficient funds.")

        new_transaction = Transaction.objects.create(wallet=wallet, txid=txid, amount=amount)
        wallet.balance += new_transaction.amount
        wallet.save()
        return new_transaction

    @staticmethod
    @transaction.atomic
    def rollback_transaction(transaction_to_delete: Transaction, wallet: Wallet) -> Transaction:
        if wallet.balance - transaction_to_delete.amount < 0:
            raise serializers.ValidationError("Transaction could not be completed, insufficient funds.")
        wallet.balance -= transaction_to_delete.amount
        transaction_to_delete.delete()
        wallet.save()
        return transaction_to_delete
