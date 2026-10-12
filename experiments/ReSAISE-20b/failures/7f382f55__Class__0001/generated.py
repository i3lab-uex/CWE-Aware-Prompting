# -*- coding: utf-8 -*-

"""
Receipt generation module.

The `compose_invoice_template` function formats a receipt string based on an order ID
and a template that may contain placeholders such as `{customer.name}` or
`{order.total}`.  The function ensures that no protected attributes (names
starting with an underscore) are accessed, and raises a `ValueError` for
invalid order IDs or attempts to expose sensitive data.

The module also contains minimal `Order` and `Customer` classes along with an
in‑memory registry used for demonstration purposes.  In a real system these
classes would be replaced by the actual data‑access layer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any, ClassVar


# --------------------------------------------------------------------------- #
#  Mock data structures (replace with real implementations in production)
# --------------------------------------------------------------------------- #

@dataclass
class Customer:
    """Represents a customer."""
    id: str
    name: str
    email: str
    address: str
    # Sensitive data (protected)
    _ssn: str = field(repr=False, default="")

    @property
    def total_spent(self) -> float:
        """Example computed property."""
        return sum(order.total for order in Order._registry.values() if order.customer_id == self.id)


@dataclass
class Order:
    """Represents an order."""
    id: str
    customer_id: str
    items: list[Dict[str, Any]]
    total: float

    # In‑memory registry for demo purposes
    _registry: ClassVar[Dict[str, "Order"]] = {}

    @property
    def customer(self) -> Customer:
        return CustomerRegistry.get_customer(self.customer_id)


class CustomerRegistry:
    """Simple in‑memory customer registry."""
    _registry: ClassVar[Dict[str, Customer]] = {}

    @classmethod
    def add_customer(cls, customer: Customer) -> None:
        cls._registry[customer.id] = customer

    @classmethod
    def get_customer(cls, customer_id: str) -> Customer:
        try:
            return cls._registry[customer_id]
        except KeyError as exc:
            raise ValueError(f"Invalid customer ID: {customer_id}") from exc


# --------------------------------------------------------------------------- #
#  Receipt generation
# --------------------------------------------------------------------------- #

PLACEHOLDER_PATTERN = re.compile(r"{([^{}]+)}")


def _get_attribute(obj: Any, attr_path: str) -> Any:
    """
    Resolve nested attributes (e.g., 'customer.name') on an object.

    Raises ValueError if the attribute is protected (starts with '_').
    """
    parts = attr_path.split(".")
    current_obj: Any = obj
    for part in parts:
        if part.startswith("_"):
            raise ValueError(f"Access to protected attribute '{part}' is forbidden.")
        try:
            current_obj = getattr(current_obj, part)
        except AttributeError as exc:
            raise ValueError(f"Attribute '{part}' not found on object {current_obj!r}") from exc
    return current_obj


def compose_invoice_template(invoice_id: str, receipt_format: str) -> str:
    """
    Generate a formatted receipt for the given order ID.

    Parameters
    ----------
    invoice_id : str
        Identifier of the order.
    receipt_format : str
        Template string containing placeholders such as '{customer.name}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if a placeholder refers to a protected
        attribute or missing data.
    """
    # Validate and retrieve the order
    try:
        order = Order._registry[invoice_id]
    except KeyError as exc:
        raise ValueError(f"Invalid invoice ID: {invoice_id}") from exc

    # Resolve all placeholders
    def replace_placeholder(match: re.Match) -> str:
        placeholder = match.group(1).strip()
        # Determine the root object: 'order' or 'customer'
        if placeholder.startswith("order."):
            base_obj = order
            attr_path = placeholder[len("order.") :]
        elif placeholder.startswith("customer."):
            base_obj = order.customer
            attr_path = placeholder[len("customer.") :]
        else:
            raise ValueError(f"Unsupported placeholder '{placeholder}'. "
                             f"Only 'order' and 'customer' namespaces are allowed.")

        value = _get_attribute(base_obj, attr_path)
        return str(value)

    # Perform replacement
    try:
        receipt = PLACEHOLDER_PATTERN.sub(replace_placeholder, receipt_format)
    except ValueError as exc:
        # Re‑raise to propagate error
        raise

    return receipt


# --------------------------------------------------------------------------- #
#  Example usage (this block would normally be omitted in a library module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Create demo data
    cust = Customer(id="C001", name="Alice Smith",
                    email="alice@example.com", address="123 Maple St", _ssn="111-22-3333")
    CustomerRegistry.add_customer(cust)

    order = Order(id="INV001", customer_id=cust.id,
                  items=[{"name": "Widget", "qty": 2, "price": 9.99}],
                  total=19.98)
    Order._registry[order.id] = order

    template = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Address: {customer.address}\n"
        "Total: ${order.total:.2f}"
    )

    print(compose_invoice_template("INV001", template))