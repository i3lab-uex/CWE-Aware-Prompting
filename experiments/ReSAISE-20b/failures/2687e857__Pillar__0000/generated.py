#!/usr/bin/env python3
"""
Utility to generate a transaction receipt from an order ID and a template string.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any


# --------------------------------------------------------------------------- #
#   Dummy domain classes (would normally come from the application)
# --------------------------------------------------------------------------- #

@dataclass
class Customer:
    """Represents a customer."""
    id: str
    name: str
    email: str
    address: str
    # Protected attribute – should not be exposed in the receipt.
    _ssn: str = field(repr=False, default="")

@dataclass
class Order:
    """Represents an order."""
    id: str
    customer: Customer
    total: float
    items: list[str]


# --------------------------------------------------------------------------- #
#   In‑memory order store (simulates a database or service)
# --------------------------------------------------------------------------- #

ORDER_DB: Dict[str, Order] = {}


def register_order(order: Order) -> None:
    """Register an order in the in‑memory store."""
    ORDER_DB[order.id] = order


# --------------------------------------------------------------------------- #
#   Receipt generation
# --------------------------------------------------------------------------- #

_placeholder_re = re.compile(r"\{([^{}]+)\}")


def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in _placeholder_re.finditer(template)}


def _safe_getattr(obj: Any, attr: str):
    """
    Retrieve an attribute from an object, raising a ValueError if the
    attribute is protected (starts with '_') or does not exist.
    """
    if attr.startswith("_"):
        raise ValueError(f"Access to protected attribute '{attr}' is forbidden.")
    if not hasattr(obj, attr):
        raise ValueError(f"Attribute '{attr}' not found on {obj.__class__.__name__}.")
    return getattr(obj, attr)


def create_transaction_receipt(transaction_id: str, temp_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the supplied
    template.

    Parameters
    ----------
    transaction_id : str
        The unique identifier of the order.
    temp_format : str
        A template string containing placeholders like '{customer.name}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid, or if a placeholder refers to a protected
        attribute.
    """
    # --------------------------------------------------------------------- #
    # 1. Retrieve the order – do not modify it.
    # --------------------------------------------------------------------- #
    order = ORDER_DB.get(transaction_id)
    if order is None:
        raise ValueError(f"Order with ID '{transaction_id}' not found.")

    # --------------------------------------------------------------------- #
    # 2. Prepare a mapping of placeholders to values.
    # --------------------------------------------------------------------- #
    placeholder_values: Dict[str, Any] = {}

    for placeholder in _extract_placeholders(temp_format):
        # Split into components (e.g., 'customer.name' -> ['customer', 'name'])
        parts = placeholder.split(".")
        if not parts:
            continue

        # Resolve the base object (order or customer)
        current_obj: Any = order
        try:
            for part in parts[1:]:
                if isinstance(current_obj, Order):
                    # For Order, attributes are accessed directly
                    current_obj = _safe_getattr(current_obj, part)
                elif isinstance(current_obj, Customer):
                    current_obj = _safe_getattr(current_obj, part)
                else:
                    # Unsupported nested type
                    raise ValueError(f"Unsupported object type in placeholder '{placeholder}'.")
            # The final resolved value
            placeholder_values[placeholder] = current_obj
        except ValueError as exc:
            # Re‑raise with context
            raise ValueError(f"Error processing placeholder '{placeholder}': {exc}") from exc

    # --------------------------------------------------------------------- #
    # 3. Perform safe formatting
    # --------------------------------------------------------------------- #
    try:
        receipt = temp_format.format_map(placeholder_values)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder value for {exc}") from exc

    return receipt


# --------------------------------------------------------------------------- #
#   Example usage (for demonstration; would normally be in a separate test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Setup sample data
    cust = Customer(id="c001", name="Alice Smith", email="alice@example.com",
                    address="123 Maple St", _ssn="123-45-6789")
    order = Order(id="o1001", customer=cust, total=249.99,
                  items=["Laptop", "Mouse"])
    register_order(order)

    # Define a template
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Address: {customer.address}\n"
        "Items:\n{items}\n"
        "Total: ${order.total:.2f}"
    )

    # Generate receipt
    try:
        print(create_transaction_receipt("o1001", tmpl))
    except ValueError as e:
        print(f"Error: {e}")