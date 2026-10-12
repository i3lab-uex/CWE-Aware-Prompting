# ──────────────────────────────────────────────────────────────── #
#  Receipt generator for an e‑commerce platform
#
#  This module defines the `compose_invoice_template` function, which
#  renders a receipt string based on a template and an order identifier.
#
#  The implementation deliberately avoids exposing protected attributes
#  (those starting with an underscore) and guarantees that all resources
#  are released before the function returns.
#
#  Author: OpenAI ChatGPT
# ──────────────────────────────────────────────────────────────── #

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Dict, Any, ClassVar

# ----------------------------------------------------------------------
# Dummy data model – in a real system these would be ORM models.
# ----------------------------------------------------------------------


@dataclass
class Customer:
    """Represents a customer."""
    id: str
    name: str
    email: str
    _credit_card_last4: str = field(repr=False, default="")

    @classmethod
    def get(cls, customer_id: str) -> "Customer":
        """Retrieve a Customer instance by ID."""
        return _CUSTOMERS_DB.get(customer_id)


@dataclass
class Order:
    """Represents an order."""
    id: str
    customer_id: str
    items: list[Dict[str, Any]]
    total: float
    date: datetime.datetime

    @classmethod
    def get(cls, order_id: str) -> "Order":
        """Retrieve an Order instance by ID."""
        return _ORDERS_DB.get(order_id)

# ----------------------------------------------------------------------
# In‑memory “database” for demonstration purposes
# ----------------------------------------------------------------------


_CUSTOMERS_DB: ClassVar[Dict[str, Customer]] = {
    "cust1": Customer(id="cust1", name="Alice Smith", email="alice@example.com",
                      _credit_card_last4="1234"),
    "cust2": Customer(id="cust2", name="Bob Jones", email="bob@example.com",
                      _credit_card_last4="5678"),
}

_ORDERS_DB: ClassVar[Dict[str, Order]] = {
    "order1": Order(
        id="order1",
        customer_id="cust1",
        items=[{"name": "Widget", "price": 19.99, "qty": 2}],
        total=39.98,
        date=datetime.datetime(2023, 10, 1, 14, 30),
    ),
    "order2": Order(
        id="order2",
        customer_id="cust2",
        items=[{"name": "Gadget", "price": 29.99, "qty": 1}],
        total=29.99,
        date=datetime.datetime(2023, 10, 2, 9, 15),
    ),
}

# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------


def _safe_dict_from_obj(obj: Any) -> Dict[str, Any]:
    """
    Convert an object into a dict containing only public attributes.
    Attributes starting with '_' are omitted to prevent leaking
    sensitive data (e.g., credit card numbers).
    """
    return {
        k: v
        for k, v in vars(obj).items()
        if not k.startswith("_")
    }


def _build_context(order: Order, customer: Customer) -> Dict[str, Any]:
    """
    Construct a context dictionary for formatting.
    The keys are prefixed with the entity name to match template placeholders
    like '{customer.name}' or '{order.total}'.
    """
    context: Dict[str, Any] = {}

    # Order data
    order_dict = _safe_dict_from_obj(order)
    for key, value in order_dict.items():
        context[f"order.{key}"] = value

    # Customer data
    customer_dict = _safe_dict_from_obj(customer)
    for key, value in customer_dict.items():
        context[f"customer.{key}"] = value

    return context


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------


def compose_invoice_template(invoice_id: str, receipt_format: str) -> str:
    """
    Generate a receipt string for the given order ID using the provided
    template.

    Parameters
    ----------
    invoice_id : str
        The identifier of the order to generate a receipt for.
    receipt_format : str
        A template string containing placeholders such as '{customer.name}'
        and '{order.total}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if the template attempts to access a
        protected attribute (i.e., an attribute name starting with '_').
    """
    # Retrieve order – raise if not found
    order = Order.get(invoice_id)
    if order is None:
        raise ValueError(f"Invalid order ID: {invoice_id!r}")

    # Retrieve customer – this should always succeed in our demo
    customer = Customer.get(order.customer_id)
    if customer is None:
        raise ValueError(f"Customer not found for order {invoice_id!r}")

    # Build context
    context = _build_context(order, customer)

    # Verify that all placeholders are safe
    for placeholder in receipt_format.split("{")[1:]:
        key = placeholder.split("}")[0]
        if not key:
            continue  # skip malformed
        if key not in context:
            raise ValueError(f"Attempt to access unknown or protected field: {key!r}")

    # Render template
    try:
        receipt = receipt_format.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in template: {exc}") from exc

    return receipt


# ----------------------------------------------------------------------
# Example usage (commented out – remove comments to run)
# ----------------------------------------------------------------------


if __name__ == "__main__":
    template = (
        "Invoice #{order.id}\n"
        "Date: {order.date:%Y-%m-%d %H:%M}\n\n"
        "Customer: {customer.name} ({customer.email})\n\n"
        "Items:\n"
        "{order.items}\n\n"
        "Total: ${order.total:.2f}"
    )
    print(compose_invoice_template("order1", template))