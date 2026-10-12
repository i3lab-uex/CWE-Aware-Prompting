#!/usr/bin/env python3
"""
create_user_receipt module

This module provides a single function, :func:`create_user_receipt`, which
generates a receipt for an e‑commerce order.  The function takes an order ID and
a template string containing placeholders that reference attributes of the
order or its associated customer.  The function safely resolves those
placeholders and returns a fully formatted receipt.

The implementation is intentionally self‑contained for demonstration purposes.
In a real application the :class:`Order` and :class:`User` classes would be
provided by your data‑access layer, and the database session management
would be handled by a framework such as SQLAlchemy.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict

# --------------------------------------------------------------------------- #
# Dummy data‑access layer – replace with real implementations in production
# --------------------------------------------------------------------------- #

@dataclass
class User:
    """Represents a customer."""
    id: str
    name: str
    email: str
    # Sensitive data that must not be exposed via receipts
    _credit_card_number: str = field(repr=False, default="")

@dataclass
class Order:
    """Represents an order."""
    id: str
    total: float
    currency: str
    customer_id: str

# In‑memory store to simulate a database
_fake_db_orders: Dict[str, Order] = {
    "ORD123": Order(id="ORD123", total=99.99, currency="USD", customer_id="USR001"),
}
_fake_db_users: Dict[str, User] = {
    "USR001": User(id="USR001", name="Alice Smith", email="alice@example.com",
                   _credit_card_number="4111111111111111"),
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_order(order_id: str) -> Order:
    """Retrieve an order by ID, raising ValueError if not found."""
    order = _fake_db_orders.get(order_id)
    if order is None:
        raise ValueError(f"Order ID '{order_id}' does not exist.")
    return order

def _get_user(user_id: str) -> User:
    """Retrieve a user by ID, raising ValueError if not found."""
    user = _fake_db_users.get(user_id)
    if user is None:
        raise ValueError(f"User ID '{user_id}' does not exist.")
    return user

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

_PLACEHOLDER_RE = re.compile(r"{(?P<path>[^}]+)}")

def create_user_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string by replacing placeholders in *template*
    with data from the order and its associated customer.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        Receipt template containing placeholders such as `{customer.name}` or
        `{order.total}`.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if a placeholder references restricted
        data (e.g., private attributes).
    """
    # Retrieve order and customer data safely
    order = _get_order(order_id)
    user  = _get_user(order.customer_id)

    # Build a mapping for placeholder resolution
    safe_map: Dict[str, Any] = {
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "order.currency": order.currency,
        "customer.id": user.id,
        "customer.name": user.name,
        "customer.email": user.email,
    }

    # Resolve placeholders
    def _replace(match: re.Match) -> str:
        key = match.group("path")
        if key not in safe_map:
            # Disallow access to private or non‑existent attributes
            raise ValueError(f"Invalid or restricted placeholder: '{key}'")
        return safe_map[key]

    # Use re.sub to perform all replacements
    receipt = _PLACEHOLDER_RE.sub(_replace, template)

    return receipt

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: {order.total} {order.currency}\n"
    )
    try:
        print(create_user_receipt("ORD123", tmpl))
    except ValueError as exc:
        print(f"Error: {exc}")