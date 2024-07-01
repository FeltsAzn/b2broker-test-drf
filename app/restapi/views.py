from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet,
    CharFilter,
    NumberFilter,
    OrderingFilter
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Wallet, Transaction
from .serializers import WalletModelSerializer, TransactionSerializer
from .services.transaction_service import TransactionService


class WalletViewFilter(FilterSet):
    label = CharFilter(lookup_expr="icontains")
    balance_from = NumberFilter(field_name="balance", lookup_expr="gte")
    order_by = OrderingFilter(fields=("balance",))

    class Meta:
        model = Wallet
        fields = ["label", "balance_from"]


class WalletView(viewsets.ModelViewSet):
    queryset = Wallet.objects.prefetch_related("transactions").all()
    serializer_class = WalletModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WalletViewFilter
    filterset_fields = ["balance", "label"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def perform_destroy(self, instance: Wallet) -> WalletModelSerializer:
        # if deleted wallet -> all transactions bind to this wallet will delete
        instance_id = instance.id
        instance.delete()
        instance.id = instance_id  # is set direct because after deleting it will be null
        return self.get_serializer(instance)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "label",
                openapi.IN_QUERY,
                description="Filter by label",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "balance_from",
                openapi.IN_QUERY,
                description="Filter by balance",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                "order_by",
                openapi.IN_QUERY,
                description="Order result by balance",
                type=openapi.TYPE_STRING,
                enum=["balance", "-balance"],
            ),
        ],
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)


class TransactionFilter(FilterSet):
    txid = CharFilter(lookup_expr="icontains")
    amount_from = NumberFilter(field_name="amount", lookup_expr="gte")
    order_by = OrderingFilter(fields=("amount",))

    class Meta:
        model = Transaction
        fields = ["txid", "amount_from"]


class TransactionView(viewsets.ModelViewSet):
    queryset = Transaction.objects.select_related("wallet").all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter
    filterset_fields = ["txid", "amount"]

    def get_queryset(self):
        wallet_id = self.kwargs.get('wallet_pk', None)
        if wallet_id is not None:
            return self.queryset.filter(wallet__id=wallet_id)
        return self.queryset

    def perform_create(self, serializer: TransactionSerializer) -> None:
        wallet_id = self.kwargs['wallet_pk']
        txid = serializer.validated_data.get('txid')
        amount = serializer.validated_data.get('amount')
        created = TransactionService.perform_transaction(wallet_id, txid, amount)
        serializer.instance = created

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def perform_destroy(self, instance: Transaction) -> TransactionSerializer:
        instance_id = instance.id
        deleted = TransactionService.rollback_transaction(instance, instance.wallet)
        deleted.id = instance_id  # is set direct because after deleting it will be null
        return self.get_serializer(deleted)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "txid",
                openapi.IN_QUERY,
                description="Filter by transaction ID",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "amount_from",
                openapi.IN_QUERY,
                description="Filter by amount greater or equal to amount",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                "order_by",
                openapi.IN_QUERY,
                description="Order result by amount",
                type=openapi.TYPE_STRING,
                enum=["amount", "-amount"],
            ),
        ],
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @swagger_auto_schema(auto_schema=None)  # type: ignore
    def update(self, request, *args, **kwargs):
        response = {"message": "Update function is not offered in this path."}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)  # type: ignore
    def partial_update(self, request, *args, **kwargs):
        response = {"message": "Update function is not offered in this path."}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
