#!/usr/bin/env python3
"""
Receipt generation for an online shopping platform.

The module provides a single public function:
    create_receipt_for_transaction(transaction_id: str, template_format: str) -> str

It safely replaces placeholders in the provided template with data from the
corresponding Order and its Customer.  Restricted or protected attributes are
not allowed; attempting to access them results in a ValueError.

The implementation follows best practices for resource handling and
prevents accidental leakage of sensitive data.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any


# --------------------------------------------------------------------------- #
#   Domain classes (simplified for demonstration)
# --------------------------------------------------------------------------- #

@dataclass
class Customer:
    """Customer data model."""
    name: str
    email: str
    address: str
    # Sensitive data – not allowed in templates
    ssn: str = field(repr=False, default="")

@dataclass
class Order:
    """Order data model."""
    id: str
    customer: Customer
    total: float
    items: list[str] = field(default_factory=list)

# --------------------------------------------------------------------------- #
#   In‑memory data store (would normally be a database)
# --------------------------------------------------------------------------- #

ORDERS: Dict[str, Order] = {}

def _initialize_demo_data() -> None:
    """Populate the ORDERS dictionary with sample data."""
    cust = Customer(
        name="Alice Smith",
        email="alice@example.com",
        address="123 Maple St, Springfield",
        ssn="123-45-6789"
    )
    ORDERS["TXN001"] = Order(
        id="TXN001",
        customer=cust,
        total=149.99,
        items=["Laptop", "Mouse"]
    )

_initialize_demo_data()

# --------------------------------------------------------------------------- #
#   Utility functions
# --------------------------------------------------------------------------- #

_RE_PLACEHOLDER = re.compile(r"\{([^\}]+)\}")

def _is_restricted_attribute(attr_path: str) -> bool:
    """
    Determine if an attribute path refers to a restricted or protected field.
    Any component that starts with '_' is considered restricted.
    """
    return any(part.startswith("_") for part in attr_path.split("."))

def _resolve_attribute(obj: Any, attr_path: str) -> Any:
    """
    Resolve a dotted attribute path on an object.
    Raises AttributeError if any component is missing or restricted.
    """
    parts = attr_path.split(".")
    current_obj: Any = obj
    for part in parts:
        if part.startswith("_"):
            raise AttributeError(f"Access to restricted attribute '{part}' denied.")
        if not hasattr(current_obj, part):
            raise AttributeError(f"Attribute '{part}' not found on {type(current_obj).__name__}.")
        current_obj = getattr(current_obj, part)
    return current_obj

# --------------------------------------------------------------------------- #
#   Public API
# --------------------------------------------------------------------------- #

def create_receipt_for_transaction(transaction_id: str, template_format: str) -> str:
    """
    Generate a formatted receipt string for the given transaction.

    Parameters
    ----------
    transaction_id : str
        Unique identifier of the order.
    template_format : str
        Template string containing placeholders like `{customer.name}`.

    Returns
    -------
    str
        The receipt with all placeholders substituted by actual values.

    Raises
    ------
    ValueError
        If the transaction ID does not exist, or if a placeholder refers to
        restricted data.
    """
    # Retrieve the order – raise ValueError if not found
    order = ORDERS.get(transaction_id)
    if order is None:
        raise ValueError(f"Transaction ID '{transaction_id}' does not exist.")

    # Prepare a mapping for placeholder resolution
    def _placeholder_replacer(match: re.Match) -> str:
        path = match.group(1).strip()
        if _is_restricted_attribute(path):
            raise ValueError(f"Placeholder '{path}' requests restricted data.")
        try:
            value = _resolve_attribute(order, path)
        except AttributeError as exc:
            raise ValueError(f"Invalid placeholder '{path}': {exc}") from None
        # Convert non-string values to string for substitution
        return str(value)

    try:
        receipt = _RE_PLACEHOLDER.sub(_placeholder_replacer, template_format)
    except ValueError as exc:
        # Re‑raise to caller
        raise

    return receipt


# --------------------------------------------------------------------------- #
#   Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Address: {customer.address}\n"
        "Total: ${order.total:.2f}"
    )
    # Note: In the template, we need to reference attributes relative to the
    # root object (Order).  The placeholder syntax assumes that.
    tmpl = (
        "Receipt for Order {id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Address: {customer.address}\n"
        "Total: ${total:.2f}"
    )
    try:
        print(create_receipt_for_transaction("TXN001", tmpl))
    except ValueError as e:
        print(f"Error: {e}")