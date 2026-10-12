# -*- coding: utf-8 -*-
"""
Receipt generation module for an e‑commerce system.

The public function `generate_buyer_receipt` accepts an order identifier and a
template string. The template may contain placeholders such as
``{customer.name}`` or ``{order.total}``. The function resolves these
placeholders from the corresponding Order and Customer objects and returns
the formatted receipt.

The implementation includes minimal security checks:
* The order ID must exist in the system.
* Certain customer attributes (e.g. `email`, `phone`) are considered
  restricted and will raise a ValueError if the template tries to use them.

This module is intentionally self‑contained for demonstration purposes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Any


# --------------------------------------------------------------------------- #
#  Data model – in a real system these would be defined elsewhere and loaded
#  from a database or service.
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Customer:
    id: str
    name: str
    address: str
    email: str  # restricted field
    phone: str  # restricted field


@dataclass(frozen=True)
class Order:
    id: str
    customer_id: str
    total: float
    items: list[str]
    date: str


# --------------------------------------------------------------------------- #
#  In‑memory repositories – replace with real persistence in production.
# --------------------------------------------------------------------------- #

_CUSTOMERS: Dict[str, Customer] = {
    "c001": Customer(
        id="c001",
        name="Alice Smith",
        address="123 Maple Street, Springfield",
        email="alice@example.com",
        phone="+1-555-0123",
    ),
    "c002": Customer(
        id="c002",
        name="Bob Johnson",
        address="456 Oak Avenue, Metropolis",
        email="bob@example.com",
        phone="+1-555-0456",
    ),
}

_ORDERS: Dict[str, Order] = {
    "o1001": Order(
        id="o1001",
        customer_id="c001",
        total=59.99,
        items=["T‑shirt", "Mug"],
        date="2024-07-21",
    ),
    "o1002": Order(
        id="o1002",
        customer_id="c002",
        total=129.49,
        items=["Laptop", "Mouse"],
        date="2024-07-22",
    ),
}


# --------------------------------------------------------------------------- #
#  Helper utilities
# --------------------------------------------------------------------------- #

_REPLACE_PATTERN = re.compile(r"\{(?P<obj>[a-zA-Z_][a-zA-Z0-9_]*)\.(?P<attr>[a-zA-Z_][a-zA-Z0-9_]*)\}")

_RESTRICTED_CUSTOMER_ATTRS = {"email", "phone"}


def _resolve_placeholder(match: re.Match, context: Dict[str, Any]) -> str:
    """Return the string value for a single placeholder."""
    obj_name = match.group("obj")
    attr_name = match.group("attr")

    if obj_name not in context:
        raise ValueError(f"Unknown placeholder object: '{obj_name}'")

    obj = context[obj_name]
    if not hasattr(obj, attr_name):
        raise ValueError(f"Attribute '{attr_name}' not found on {obj_name}")

    if obj_name == "customer" and attr_name in _RESTRICTED_CUSTOMER_ATTRS:
        raise ValueError(f"Access to restricted customer attribute '{attr_name}' is not allowed")

    return str(getattr(obj, attr_name))


# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #

def generate_buyer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the buyer based on a given template.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        Receipt pattern containing placeholders in the form `{object.attribute}`.

    Returns
    -------
    str
        Formatted receipt string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the order ID is invalid, or if restricted customer data is requested.
    """
    # Retrieve the order
    try:
        order = _ORDERS[order_id]
    except KeyError as exc:
        raise ValueError(f"Invalid order ID: {order_id}") from exc

    # Retrieve the customer
    try:
        customer = _CUSTOMERS[order.customer_id]
    except KeyError as exc:
        raise ValueError(f"Customer for order '{order_id}' not found") from exc

    # Build the context dictionary
    context = {
        "order": order,
        "customer": customer,
    }

    # Replace placeholders safely
    try:
        receipt = _REPLACE_PATTERN.sub(lambda m: _resolve_placeholder(m, context), template)
    except ValueError as exc:
        # Re‑raise with a clearer message
        raise ValueError(f"Template processing error: {exc}") from exc

    return receipt


# --------------------------------------------------------------------------- #
#  Example usage (for demonstration only – remove or guard with if __name__ == "__main__")
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Date: {order.date}\n"
        "Customer: {customer.name}\n"
        "Address: {customer.address}\n"
        "Items: {order.items}\n"
        "Total: ${order.total:.2f}"
    )
    print(generate_buyer_receipt("o1001", tmpl))