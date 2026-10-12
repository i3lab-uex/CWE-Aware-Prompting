#!/usr/bin/env python3
"""
A minimal implementation of a receipt generator for an e‑commerce platform.
"""

from __future__ import annotations

import re
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Domain models – simplified stubs for Order and Customer
# --------------------------------------------------------------------------- #

class Customer:
    """
    Represents a customer. Protected attributes (starting with an underscore)
    are considered sensitive and must not be exposed via the receipt template.
    """
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email          # public
        self.phone = phone          # public
        self._ssn = "123-45-6789"   # protected

    def __repr__(self) -> str:
        return f"<Customer {self.name}>"


class Order:
    """
    Represents an order. Contains a reference to the customer and order details.
    """
    def __init__(self, order_id: str, customer: Customer, total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total

    def __repr__(self) -> str:
        return f"<Order {self.order_id}>"


# --------------------------------------------------------------------------- #
# In‑memory "database" of orders
# --------------------------------------------------------------------------- #

ORDER_DB: Dict[str, Order] = {}


def register_order(order: Order) -> None:
    """Store an order in the in‑memory database."""
    ORDER_DB[order.order_id] = order


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

PLACEHOLDER_RE = re.compile(r"{(?P<path>[\w\.]+)}")


def _resolve_path(obj: Any, path: str) -> Any:
    """
    Resolve a dotted attribute path on an object.
    Raises ValueError if the attribute is protected (starts with '_').
    """
    parts = path.split(".")
    for part in parts:
        if getattr(obj, part, None) is None:
            raise ValueError(f"Attribute '{part}' not found in object {obj!r}")
        if part.startswith("_"):
            raise ValueError(f"Attempt to access protected attribute '{part}'")
        obj = getattr(obj, part)
    return obj


def _safe_format(template: str, mapping: Dict[str, Any]) -> str:
    """
    Replace placeholders in the template with values from mapping.
    Raises ValueError if a placeholder cannot be resolved or refers to
    protected data.
    """
    def repl(match: re.Match) -> str:
        path = match.group("path")
        if path not in mapping:
            # Attempt to resolve the path lazily
            try:
                value = _resolve_path(mapping["root"], path)
                mapping[path] = value
            except Exception as exc:
                raise ValueError(f"Unable to resolve placeholder '{{{path}}}': {exc}") from exc
        return str(mapping[path])

    return PLACEHOLDER_RE.sub(repl, template)


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_transaction_receipt(transaction_id: str, temp_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the supplied
    template. The template may contain placeholders like '{customer.name}' or
    '{order.total}'. Protected attributes (starting with an underscore) are not
    allowed and will raise a ValueError.

    Parameters:
        transaction_id (str): The ID of the order to retrieve.
        temp_format (str): The template string for the receipt.

    Returns:
        str: The formatted receipt.

    Raises:
        ValueError: If the transaction ID is invalid or if a protected
                    attribute is accessed.
    """
    # ------------------------------------------------------------------ #
    # 1. Retrieve the order – this simulates opening a resource
    # ------------------------------------------------------------------ #
    order = ORDER_DB.get(transaction_id)
    if not order:
        raise ValueError(f"Invalid transaction ID: {transaction_id!r}")

    # ------------------------------------------------------------------ #
    # 2. Prepare the context for template substitution
    # ------------------------------------------------------------------ #
    context = {
        "root": order,           # root object for dotted lookups
        "order": order,
        "customer": order.customer,
    }

    # ------------------------------------------------------------------ #
    # 3. Perform the safe formatting
    # ------------------------------------------------------------------ #
    receipt = _safe_format(temp_format, context)

    # ------------------------------------------------------------------ #
    # 4. Release the resource – in this simple example nothing special is
    #    required, but we explicitly delete references to avoid accidental
    #    retention.
    # ------------------------------------------------------------------ #
    del order
    return receipt


# --------------------------------------------------------------------------- #
# Example usage – this block is executed only when running the script directly
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Create sample data
    cust = Customer(name="Alice Smith", email="alice@example.com", phone="555-1234")
    order = Order(order_id="ORD001", customer=cust, total=149.99)
    register_order(order)

    # Define a template
    tmpl = (
        "Receipt for Order {order.order_id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Phone: {customer.phone}\n"
        "Total: ${order.total:.2f}"
    )

    # Generate receipt
    try:
        print(create_transaction_receipt("ORD001", tmpl))
    except ValueError as e:
        print(f"Error generating receipt: {e}")