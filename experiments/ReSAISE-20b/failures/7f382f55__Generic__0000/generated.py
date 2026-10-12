# ------------------------------------------------------------
# Receipt generation module for an e-commerce platform.
#
# The core function `compose_invoice_template` accepts an order
# identifier and a receipt format string containing placeholders.
#
# Security considerations:
#   * Only whitelisted fields of Order and Customer are allowed
#     in the template.
#   * Attempts to access any attribute that starts with an underscore
#     (treated as protected) raise a ValueError.
#
# ------------------------------------------------------------
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any, ClassVar

# ------------------------------------------------------------
# Simple in‑memory data models
# ------------------------------------------------------------

@dataclass
class Customer:
    id: str
    name: str
    email: str

    # Example of a protected attribute that should not be exposed.
    _ssn: str = field(repr=False, default="")

@dataclass
class Order:
    id: str
    customer: Customer
    total: float
    items: list[str]

    # In‑memory registry of orders.
    _registry: ClassVar[Dict[str, "Order"]] = {}

    @classmethod
    def register(cls, order: "Order") -> None:
        cls._registry[order.id] = order

    @classmethod
    def get_by_id(cls, order_id: str) -> "Order":
        try:
            return cls._registry[order_id]
        except KeyError as exc:
            raise ValueError(f"Invalid order ID: {order_id}") from exc


# ------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------

_PLACEHOLDER_RE = re.compile(r"{(?P<key>[^}]+)}")

def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder keys found in the template."""
    return {m.group("key") for m in _PLACEHOLDER_RE.finditer(template)}

def _build_context(order: Order) -> Dict[str, Any]:
    """Create a flat context dictionary for formatting."""
    ctx: Dict[str, Any] = {
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "order.items": ", ".join(order.items),
    }

    # Customer fields
    cust = order.customer
    ctx.update(
        {
            "customer.id": cust.id,
            "customer.name": cust.name,
            "customer.email": cust.email,
        }
    )
    return ctx


# ------------------------------------------------------------
# Main function
# ------------------------------------------------------------

def compose_invoice_template(invoice_id: str, receipt_format: str) -> str:
    """
    Generate a receipt string based on the provided format template.

    Parameters
    ----------
    invoice_id : str
        The identifier of the order.
    receipt_format : str
        Template string containing placeholders like '{customer.name}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if a protected attribute is accessed.
    """
    # Retrieve order
    order = Order.get_by_id(invoice_id)

    # Extract placeholders from the template
    placeholders = _extract_placeholders(receipt_format)

    # Build context mapping
    ctx = _build_context(order)

    # Validate placeholders
    for key in placeholders:
        if key not in ctx:
            raise ValueError(f"Unknown placeholder '{key}' in receipt template.")
        # Protect against accessing attributes starting with underscore
        if key.startswith("_"):
            raise ValueError(f"Access to protected attribute '{key}' is not allowed.")

    # Perform formatting
    try:
        return receipt_format.format(**ctx)
    except KeyError as exc:  # pragma: no cover
        raise ValueError(f"Missing data for placeholder {exc.args[0]!r}") from exc


# ------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ------------------------------------------------------------

if __name__ == "__main__":
    # Create sample data
    cust = Customer(id="C001", name="Alice Smith", email="alice@example.com")
    order = Order(
        id="O123",
        customer=cust,
        total=149.99,
        items=["Widget A", "Gadget B"],
    )
    Order.register(order)

    # Define a receipt template
    template = (
        "Receipt #{order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Items: {order.items}\n"
        "Total: ${order.total}"
    )

    # Generate receipt
    print(compose_invoice_template("O123", template))