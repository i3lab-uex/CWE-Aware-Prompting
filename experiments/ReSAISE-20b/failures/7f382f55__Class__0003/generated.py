#!/usr/bin/env python3
"""
Utility to compose a customer invoice from a template string.

The module assumes the existence of two domain classes, `Order` and
`Customer`, and a simple in‑memory registry that maps order IDs to
`Order` objects.  The function `compose_invoice_template` replaces a
limited set of placeholders in the supplied template with real data.
Only safe, non‑sensitive fields are allowed; attempting to reference
protected attributes (e.g. SSN, credit card numbers) raises a
`ValueError`.

The implementation protects against CWE‑200 (Information Exposure)
by explicitly whitelisting permissible placeholders and rejecting
any that could leak sensitive data.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any

# ----------------------------------------------------------------------
# Domain model (minimal stubs for illustration)
# ----------------------------------------------------------------------
@dataclass
class Customer:
    """Represents a customer."""
    name: str
    email: str
    # Sensitive fields that must not be exposed via the template
    ssn: str | None = field(repr=False, default=None)
    credit_card_number: str | None = field(repr=False, default=None)


@dataclass
class Order:
    """Represents an order."""
    id: str
    total: float
    items: list[str]
    customer: Customer


# ----------------------------------------------------------------------
# In‑memory order registry
# ----------------------------------------------------------------------
ORDERS_REGISTRY: Dict[str, Order] = {}


def register_order(order: Order) -> None:
    """Register an order so that it can be retrieved by ID."""
    ORDERS_REGISTRY[order.id] = order


def get_order_by_id(order_id: str) -> Order:
    """Retrieve an order by its ID, raising ValueError if not found."""
    try:
        return ORDERS_REGISTRY[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' not found.") from exc


# ----------------------------------------------------------------------
# Template composition
# ----------------------------------------------------------------------
# Whitelist of allowed placeholders.
_ALLOWED_PLACEHOLDERS = {
    "customer.name",
    "customer.email",
    "order.total",
    "order.items",
}

# Regex to find placeholders of the form {key}
_PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")


def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholders found in the template."""
    return {match.group(1) for match in _PLACEHOLDER_RE.finditer(template)}


def _build_context(order: Order) -> Dict[str, Any]:
    """Construct a mapping from placeholder names to values."""
    return {
        "customer.name": order.customer.name,
        "customer.email": order.customer.email,
        "order.total": f"{order.total:.2f}",
        "order.items": ", ".join(order.items),
    }


def compose_invoice_template(invoice_id: str, receipt_format: str) -> str:
    """
    Generate a receipt string from a template.

    Parameters
    ----------
    invoice_id : str
        The unique identifier of the order.
    receipt_format : str
        Template string containing placeholders.

    Returns
    -------
    str
        The formatted receipt.

    Raises
    ------
    ValueError
        If the order ID is invalid or if the template references disallowed
        placeholders that could expose sensitive information.
    """
    # Validate and retrieve the order
    order = get_order_by_id(invoice_id)

    # Find all placeholders in the template
    placeholders = _extract_placeholders(receipt_format)

    # Check for disallowed placeholders
    if not placeholders.issubset(_ALLOWED_PLACEHOLDERS):
        disallowed = placeholders - _ALLOWED_PLACEHOLDERS
        raise ValueError(
            f"Template contains disallowed placeholders: {', '.join(disallowed)}"
        )

    # Build context and perform substitution
    context = _build_context(order)

    try:
        receipt = receipt_format.format(**context)
    except KeyError as exc:
        # This should not happen because we validated placeholders
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return receipt


# ----------------------------------------------------------------------
# Example usage (commented out – remove comments to run)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Create a customer and order
    cust = Customer(name="Jane Doe", email="jane@example.com", ssn="123-45-6789")
    order = Order(id="INV001", total=149.99, items=["Widget A", "Widget B"], customer=cust)

    # Register the order
    register_order(order)

    # Define a template
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total}\n"
        "Items: {order.items}"
    )

    # Compose the receipt
    try:
        print(compose_invoice_template("INV001", tmpl))
    except ValueError as e:
        print(f"Error: {e}")