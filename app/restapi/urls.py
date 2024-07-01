from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import WalletView, TransactionView

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

wallet_list = WalletView.as_view({
    "get": "list",
    "post": "create"
})

wallet_detail = WalletView.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy"
})

transaction_list = TransactionView.as_view({
    "get": "list",
    "post": "create"
})

transaction_detail = TransactionView.as_view(
    {
        "get": "retrieve",
        "delete": "destroy"
    }
)
urlpatterns = [
    path("wallets/", wallet_list, name="wallets"),
    path("wallets/<int:pk>/", wallet_detail, name="wallet-detail"),
    path("wallets/<int:wallet_pk>/transactions/", transaction_list, name="wallet-transactions"),
    path("wallets/<int:wallet_pk>/transactions/<int:pk>", transaction_detail, name="wallet-transaction-detail"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),  # type: ignore
]
