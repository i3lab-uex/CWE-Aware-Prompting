# -*- coding: utf-8 -*-
"""
Receipt generation module for an e‑commerce application.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict


# --------------------------------------------------------------------------- #
# Mocked domain objects (in real code these would be imported from the app)
# --------------------------------------------------------------------------- #
@dataclass
class Customer:
    """Represents a customer."""
    id: str
    name: str
    email: str
    phone: str | None = None
    # Flag indicating whether the customer has restricted data access.
    restricted: bool = False

    def can_access(self) -> bool:
        """Return True if the customer data is not restricted."""
        return not self.restricted


@dataclass
class Order:
    """Represents an order."""
    id: str
    total: float
    currency: str
    customer_id: str

# --------------------------------------------------------------------------- #
# Mocked persistence layer (replace with real DB access in production)
# --------------------------------------------------------------------------- #
_CUSTOMERS_DB: Dict[str, Customer] = {
    "cust_001": Customer(id="cust_001", name="Alice Smith", email="alice@example.com"),
    "cust_002": Customer(id="cust_002", name="Bob Jones", email="bob@example.com", restricted=True),
}

_ORDERS_DB: Dict[str, Order] = {
    "order_123": Order(id="order_123", total=99.95, currency="USD", customer_id="cust_001"),
    "order_456": Order(id="order_456", total=149.50, currency="EUR", customer_id="cust_002"),
}


def _get_order(order_id: str) -> Order:
    """Retrieve an order from the database."""
    try:
        return _ORDERS_DB[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' is invalid.") from exc


def _get_customer(customer_id: str) -> Customer:
    """Retrieve a customer from the database."""
    try:
        return _CUSTOMERS_DB[customer_id]
    except KeyError as exc:
        raise ValueError(f"Customer ID '{customer_id}' not found.") from exc


# --------------------------------------------------------------------------- #
# Receipt generation
# --------------------------------------------------------------------------- #
PLACEHOLDER_PATTERN = re.compile(r"{(?P<key>[^}]+)}")


def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    return {match.group("key") for match in PLACEHOLDER_PATTERN.finditer(template)}


def _build_context(order: Order, customer: Customer) -> Dict[str, Any]:
    """
    Build a context dictionary for template formatting.
    Only includes attributes that are allowed to be exposed.
    """
    # Base context
    ctx: Dict[str, Any] = {
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "order.currency": order.currency,
    }

    # Customer context
    if customer.can_access():
        ctx.update(
            {
                "customer.id": customer.id,
                "customer.name": customer.name,
                "customer.email": customer.email,
            }
        )
    else:
        # Restricted data: do not expose any customer attributes
        ctx.update(
            {
                "customer.id": "RESTRICTED",
                "customer.name": "RESTRICTED",
                "customer.email": "RESTRICTED",
            }
        )
    return ctx


def generate_client_receipt(order_id: str, template: str) -> str:
    """
    Generate a formatted receipt for the given order ID using the provided template.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A string containing placeholders such as '{customer.name}' and '{order.total}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if restricted customer data is attempted to be accessed.
    """
    # Retrieve domain objects
    order = _get_order(order_id)
    customer = _get_customer(order.customer_id)

    # Security check: reject if the template attempts to access restricted data
    placeholders = _extract_placeholders(template)
    if "customer.email" in placeholders and customer.restricted:
        raise ValueError("Attempt to access restricted customer data.")

    # Build context for formatting
    context = _build_context(order, customer)

    try:
        receipt = template.format(**context)
    except KeyError as exc:
        # A placeholder was not found in the context
        missing = exc.args[0]
        raise ValueError(f"Missing placeholder data for '{missing}'.") from exc

    return receipt