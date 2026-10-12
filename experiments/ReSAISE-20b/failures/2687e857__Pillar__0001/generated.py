#!/usr/bin/env python3
"""
Module: receipt_generator

This module provides the `create_transaction_receipt` function which formats a
receipt string based on an order ID and a template containing placeholders.
The implementation is intentionally defensive: it validates placeholder names,
prevents access to protected attributes, and handles missing orders gracefully.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Domain model definitions (minimal for demonstration purposes)
# --------------------------------------------------------------------------- #

@dataclass
class Customer:
    """Represents a customer."""
    id: str
    name: str
    email: str
    # Protected attribute – should not be exposed via the receipt template
    _ssn: str = field(repr=False, default="")

@dataclass
class Order:
    """Represents an order."""
    id: str
    customer: Customer
    total: float
    items: Dict[str, int]  # item name -> quantity


# --------------------------------------------------------------------------- #
# In‑memory data store (simulating a database)
# --------------------------------------------------------------------------- #

_orders: Dict[str, Order] = {}

def add_order(order: Order) -> None:
    """Adds an order to the in‑memory store."""
    _orders[order.id] = order

def get_order(order_id: str) -> Order:
    """Retrieves an order by its ID, raising ValueError if not found."""
    try:
        return _orders[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' does not exist.") from exc


# --------------------------------------------------------------------------- #
# Receipt generation
# --------------------------------------------------------------------------- #

_PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

def _resolve_placeholder(order: Order, placeholder: str) -> Any:
    """
    Resolve a single placeholder against the order object.
    Supports nested attributes separated by dots, e.g. 'customer.name'.
    Raises ValueError if a protected attribute is accessed.
    """
    attrs = placeholder.split(".")
    obj: Any = order
    for attr in attrs:
        # Prevent access to protected attributes (starting with an underscore)
        if attr.startswith("_"):
            raise ValueError(f"Access to protected attribute '{attr}' is not allowed.")
        if hasattr(obj, attr):
            obj = getattr(obj, attr)
        else:
            raise ValueError(f"Attribute '{attr}' not found in object of type {type(obj).__name__}.")
    return obj

def create_transaction_receipt(transaction_id: str, temp_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the provided
    template. Placeholders in the format `{...}` are replaced with actual data.

    Args:
        transaction_id: The ID of the order to format.
        temp_format: Template string containing placeholders.

    Returns:
        The formatted receipt string.

    Raises:
        ValueError: If the order ID is invalid or if a placeholder references
                    protected information.
    """
    # Retrieve the order; this may raise ValueError if ID is invalid
    order = get_order(transaction_id)

    # Find all placeholders in the template
    matches = _PLACEHOLDER_RE.findall(temp_format)

    # Build a mapping from placeholder to resolved value
    resolved: Dict[str, Any] = {}
    for placeholder in matches:
        if placeholder not in resolved:
            resolved[placeholder] = _resolve_placeholder(order, placeholder)

    # Perform the substitution safely
    def replacement(match: re.Match) -> str:
        key = match.group(1)
        value = resolved.get(key, "")
        return str(value)

    receipt = _PLACEHOLDER_RE.sub(replacement, temp_format)
    return receipt


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Create a customer and an order
    cust = Customer(id="C001", name="Alice Smith", email="alice@example.com", _ssn="123-45-6789")
    order = Order(id="O1001", customer=cust, total=199.99, items={"Laptop": 1, "Mouse": 2})
    add_order(order)

    # Define a template
    tmpl = (
        "Receipt for Order {id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total Amount: ${total}\n"
        "Items:\n"
    )
    for item, qty in order.items.items():
        tmpl += f"  - {item}: {qty}\n"

    # Generate receipt
    print(create_transaction_receipt("O1001", tmpl))