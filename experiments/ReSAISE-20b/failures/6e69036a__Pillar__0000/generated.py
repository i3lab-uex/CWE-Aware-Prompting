# -*- coding: utf-8 -*-
"""
Receipt generation module.

This module defines the `generate_client_receipt` function that produces a
formatted receipt for an e‑commerce order.  The implementation takes care of:
* Safe lookup and cleanup of the underlying data store.
* Validation that an order exists and that the customer data is accessible.
* Using Python's `str.format` in a controlled manner so that only the
  supplied attributes can be accessed.
"""

from __future__ import annotations

import contextlib
import datetime
import uuid
from dataclasses import dataclass, field
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Data model (minimal for demonstration purposes)
# --------------------------------------------------------------------------- #

@dataclass
class Customer:
    """Represents a customer."""
    id: uuid.UUID
    name: str
    email: str
    _restricted: bool = field(default=False, repr=False)

    def __post_init__(self):
        if self._restricted:
            raise PermissionError("Attempted to instantiate restricted customer data.")


@dataclass
class Order:
    """Represents an order."""
    id: uuid.UUID
    customer: Customer
    total: float
    date: datetime.datetime


# --------------------------------------------------------------------------- #
# In‑memory data store (acts as a mock database)
# --------------------------------------------------------------------------- #

class _OrderStore:
    """A very small in‑memory store that mimics a database session."""

    _orders: Dict[uuid.UUID, Order] = {}

    @classmethod
    def add_order(cls, order: Order) -> None:
        cls._orders[order.id] = order

    @classmethod
    def get_order(cls, order_id: uuid.UUID) -> Optional[Order]:
        return cls._orders.get(order_id)


# Populate the store with a couple of sample orders
cust1 = Customer(id=uuid.uuid4(), name="Alice Smith", email="alice@example.com")
cust2 = Customer(id=uuid.uuid4(), name="Bob Johnson", email="bob@example.com")
_order1 = Order(
    id=uuid.uuid4(),
    customer=cust1,
    total=199.99,
    date=datetime.datetime.now()
)
_order2 = Order(
    id=uuid.uuid4(),
    customer=cust2,
    total=49.50,
    date=datetime.datetime.now()
)
_OrderStore.add_order(_order1)
_OrderStore.add_order(_order2)


# --------------------------------------------------------------------------- #
# Utility context manager for resource handling
# --------------------------------------------------------------------------- #

@contextlib.contextmanager
def _order_session():
    """
    Context manager that yields the order store and ensures cleanup.
    This is a simplified representation of acquiring and releasing
    resources such as database connections.  In a real application,
    this would handle transactions, connection pools, etc.
    """
    try:
        yield _OrderStore
    finally:
        # In a real scenario, close connections or release locks here.
        pass


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def generate_client_receipt(order_id: str, template: str) -> str:
    """
    Generate a formatted receipt for the given order.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order (UUID string).
    template : str
        A format string containing placeholders such as '{customer.name}'
        and '{order.total}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is not a valid UUID or if no such order exists.
    PermissionError
        If the customer data is marked as restricted and cannot be accessed.
    """
    # Validate UUID format
    try:
        uid = uuid.UUID(order_id)
    except (ValueError, AttributeError):
        raise ValueError("Invalid order ID format; must be a UUID string.") from None

    with _order_session() as store:
        order = store.get_order(uid)

        if order is None:
            raise ValueError(f"No order found for ID {order_id}.")

        # Access customer data; this may raise PermissionError if restricted
        try:
            _ = order.customer.name  # simple access to trigger any potential restrictions
        except PermissionError as exc:
            raise ValueError("Access to customer data is restricted.") from exc

        # Prepare a safe namespace for formatting
        context = {"order": order, "customer": order.customer}

        try:
            receipt = template.format(**context)
        except KeyError as exc:
            raise ValueError(f"Missing placeholder in template: {exc}") from None
        except Exception as exc:
            # Catch any unexpected formatting errors
            raise ValueError(f"Template formatting failed: {exc}") from None

        return receipt


# --------------------------------------------------------------------------- #
# Example usage (commented out to avoid side effects on import)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Receipt\n"
        "-------\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Order ID: {order.id}\n"
        "Date: {order.date:%Y-%m-%d %H:%M:%S}\n"
        "Total: ${order.total:.2f}"
    )
    print(generate_client_receipt(str(_order1.id), tmpl))