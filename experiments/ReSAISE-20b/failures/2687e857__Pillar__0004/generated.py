#!/usr/bin/env python3
"""
Utility to generate a formatted transaction receipt for an e-commerce platform.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Domain model – minimal stubs for Order and Customer
# --------------------------------------------------------------------------- #

@dataclass
class Customer:
    """Represents a customer in the system."""
    id: str
    name: str
    email: str
    _ssn: str | None = field(default=None, repr=False)  # protected attribute

    def __post_init__(self):
        if not self.id or not isinstance(self.id, str):
            raise ValueError("Customer must have a non‑empty string id.")


@dataclass
class Order:
    """Represents an order in the system."""
    id: str
    customer: Customer
    items: list[tuple[str, int, float]]  # (name, quantity, unit_price)
    total: float = field(init=False)

    def __post_init__(self):
        if not self.id or not isinstance(self.id, str):
            raise ValueError("Order must have a non‑empty string id.")
        self.total = sum(qty * price for _, qty, price in self.items)


# --------------------------------------------------------------------------- #
# In‑memory repository (simulating a data store)
# --------------------------------------------------------------------------- #

# Global registry of orders – in real code this would be replaced with a DB call
ORDERS_DB: Dict[str, Order] = {}


def register_order(order: Order) -> None:
    """Add an order to the in‑memory registry."""
    ORDERS_DB[order.id] = order


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _sanitize_template(template: str) -> None:
    """
    Basic validation of the template string to prevent code injection.
    Disallow any format fields that contain arbitrary Python expressions.
    """
    # Regex to find all format placeholders like {foo} or {bar:format}
    pattern = re.compile(r"{([^{}]+)}")
    for match in pattern.finditer(template):
        field = match.group(1)
        # Reject if field contains any disallowed characters
        if not re.fullmatch(r"[a-zA-Z0-9_.]+", field):
            raise ValueError(f"Invalid placeholder '{field}' in template.")


def _build_context(order: Order) -> Dict[str, Any]:
    """
    Construct a mapping of placeholder names to values.
    Raises ValueError if a protected attribute is requested.
    """
    context: Dict[str, Any] = {}

    # Customer data
    for attr in vars(order.customer):
        if attr.startswith("_"):
            raise ValueError(f"Access to protected attribute '{attr}' is not allowed.")
        context[f"customer.{attr}"] = getattr(order.customer, attr)

    # Order data
    for attr in vars(order):
        if attr.startswith("_"):
            continue  # skip private attributes like _total
        context[f"order.{attr}"] = getattr(order, attr)

    return context


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_transaction_receipt(transaction_id: str, temp_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the supplied
    template. Placeholders in the template are replaced with actual data.

    Parameters:
        transaction_id (str): The identifier of the order.
        temp_format (str): Template string containing placeholders like
                           '{customer.name}' or '{order.total}'.

    Returns:
        str: The formatted receipt string.

    Raises:
        ValueError: If the transaction ID is invalid, if protected
                    customer data is accessed, or if template validation fails.
    """
    # Validate transaction ID
    if not isinstance(transaction_id, str) or not transaction_id:
        raise ValueError("transaction_id must be a non‑empty string.")

    # Retrieve the order
    order = ORDERS_DB.get(transaction_id)
    if order is None:
        raise ValueError(f"No order found for transaction ID '{transaction_id}'.")

    # Sanitize the template
    _sanitize_template(temp_format)

    # Build context mapping
    context = _build_context(order)

    try:
        receipt = temp_format.format_map(context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in template: {exc}") from None

    return receipt


# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Create sample data
    cust = Customer(id="c001", name="Alice Smith", email="alice@example.com")
    order = Order(
        id="o123",
        customer=cust,
        items=[("Widget", 2, 9.99), ("Gadget", 1, 19.95)],
    )
    register_order(order)

    # Define a receipt template
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Items:\n"
        "{order.items}\n"
        "Total: ${order.total:.2f}"
    )

    # Generate receipt
    print(create_transaction_receipt("o123", tmpl))