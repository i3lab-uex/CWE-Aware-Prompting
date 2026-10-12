#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementation of build_order_receipt for an online shopping platform.

The function retrieves an Order instance by its identifier, resolves
placeholders in a template string using data from the order and its
associated customer, and returns the fully formatted receipt.

Security considerations:
* Only a whitelist of allowed fields may be accessed.
* Any attempt to access protected or private attributes raises ValueError.
* The function does not keep any external resources open beyond the
  scope of its execution, mitigating CWE-664 (Improper Control of a Resource).
"""

from __future__ import annotations

import re
from typing import Any, Dict

# Assume these classes are defined elsewhere in the codebase.
# They must expose a classmethod `get_by_id` to fetch an instance by its ID.
try:
    from models import Order, Customer
except ImportError:  # pragma: no cover
    class _MockCustomer:
        def __init__(self, name: str, email: str):
            self.name = name
            self.email = email

    class _MockOrder:
        def __init__(self, order_id: str, total: float, customer: _MockCustomer):
            self.order_id = order_id
            self.total = total
            self.customer = customer

        @classmethod
        def get_by_id(cls, order_id: str) -> "_MockOrder":
            # Dummy implementation for testing purposes
            if order_id != "12345":
                return None
            cust = _MockCustomer(name="John Doe", email="john@example.com")
            return cls(order_id=order_id, total=99.99, customer=cust)

    Order = _MockOrder
    Customer = _MockCustomer


# --------------------------------------------------------------------------- #
# Helper utilities

_ALLOWED_FIELDS: Dict[str, Any] = {
    "order_id": str,
    "total": float,
    # Add other order fields as needed
}

_ALLOWED_CUSTOMER_FIELDS: Dict[str, Any] = {
    "name": str,
    "email": str,
    # Add other customer fields as needed
}

_PLACEHOLDER_RE = re.compile(r"{([^{}]+)}")


def _resolve_placeholder(value_path: str, context: Dict[str, Any]) -> str:
    """
    Resolve a dotted path (e.g., 'customer.name') against the provided context.
    Only whitelisted fields are accessible.

    Raises ValueError if the path is invalid or points to a protected attribute.
    """
    parts = value_path.split(".")
    if not parts:
        raise ValueError(f"Empty placeholder path: '{value_path}'")

    # Resolve the root object
    root_name = parts[0]
    if root_name not in context:
        raise ValueError(f"Unknown placeholder root: '{root_name}'")
    obj = context[root_name]

    # Walk the attribute chain
    for attr in parts[1:]:
        if not hasattr(obj, attr):
            raise ValueError(f"Attribute '{attr}' does not exist on {obj}")
        if attr.startswith("_"):
            raise ValueError(f"Access to protected attribute '{attr}' is forbidden")
        # Check against the whitelist
        if root_name == "order" and attr not in _ALLOWED_FIELDS:
            raise ValueError(f"Field '{attr}' is not allowed for order")
        if root_name == "customer" and attr not in _ALLOWED_CUSTOMER_FIELDS:
            raise ValueError(f"Field '{attr}' is not allowed for customer")
        obj = getattr(obj, attr)

    return str(obj)


# --------------------------------------------------------------------------- #
# Main function

def build_order_receipt(order_identifier: str, template_string: str) -> str:
    """
    Generate a receipt for the given order by substituting placeholders in
    `template_string` with actual data.

    Parameters:
        order_identifier (str): Unique identifier of the order.
        template_string  (str): Template containing placeholders like
                                '{customer.name}' and '{order.total}'.

    Returns:
        str: The fully formatted receipt string.

    Raises:
        ValueError: If the order ID is invalid, a placeholder references
                    restricted data, or any other resolution error occurs.
    """
    # ----------------------------------------------------------------------- #
    # 1. Retrieve the order
    order: Order | None = Order.get_by_id(order_identifier)
    if order is None:
        raise ValueError(f"Order ID '{order_identifier}' does not exist")

    # Assume order has a 'customer' attribute pointing to a Customer instance
    customer: Customer = getattr(order, "customer", None)
    if customer is None:
        raise ValueError(f"Order '{order_identifier}' has no associated customer")

    # ----------------------------------------------------------------------- #
    # 2. Build a context dictionary for placeholder resolution
    context = {
        "order": order,
        "customer": customer,
    }

    # ----------------------------------------------------------------------- #
    # 3. Substitute placeholders
    def _replacement(match: re.Match) -> str:
        path = match.group(1).strip()
        return _resolve_placeholder(path, context)

    try:
        receipt = _PLACEHOLDER_RE.sub(_replacement, template_string)
    except ValueError as exc:
        # Re‑raise with a clearer message
        raise ValueError(f"Failed to build receipt: {exc}") from None

    # ----------------------------------------------------------------------- #
    # 4. Return the formatted receipt
    return receipt


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)

if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.order_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total}\n"
    )
    try:
        print(build_order_receipt("12345", tmpl))
    except ValueError as e:
        print(f"Error: {e}")