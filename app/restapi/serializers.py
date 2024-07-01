from rest_framework import serializers

from .models import Wallet, Transaction


class WalletModelSerializer(serializers.ModelSerializer):
    label = serializers.CharField(required=False)

    class Meta:
        model = Wallet
        fields = ["id", "label", "balance"]
        read_only_fields = ["balance"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "wallet", "txid", "amount"]
        read_only_fields = ["wallet"]

    def validate_amount(self, value):
        if value == 0:
            raise serializers.ValidationError("Amount cannot be zero")
        return value
