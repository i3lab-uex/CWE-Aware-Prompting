#!/usr/bin/env python3
"""
Module: receipt_generator

This module provides a single function, `create_order_receipt`, which
generates a formatted receipt string for an online shopping order.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any


# ----------------------------------------------------------------------
# Mock data models (in a real system these would be ORM models)
# ----------------------------------------------------------------------


@dataclass
class Customer:
    id: str
    name: str
    email: str
    address: str
    # Sensitive attributes that must not be exposed via the receipt
    password: str = field(repr=False, default="***")
    ssn: str = field(repr=False, default="***")


@dataclass
class Order:
    id: str
    total: float
    date: str  # ISO format
    items: List[Dict[str, Any]]
    customer_id: str

    # In a real system this would query the database
    _registry: Dict[str, "Order"] = field(default_factory=dict, init=False, repr=False)

    @classmethod
    def register(cls, order: "Order"):
        cls._registry[order.id] = order

    @classmethod
    def get_by_id(cls, order_id: str) -> "Order | None":
        return cls._registry.get(order_id)


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------


def _allowed_customer_attrs() -> set[str]:
    """Return a set of customer attributes that are safe to expose."""
    return {"name", "email", "address"}


def _allowed_order_attrs() -> set[str]:
    """Return a set of order attributes that are safe to expose."""
    return {"id", "total", "date"}


def _resolve_placeholder(
    placeholder: str,
    order: Order,
    customer: Customer,
) -> Any:
    """
    Resolve a single placeholder of the form 'object.attribute'.
    Raises ValueError if the attribute is not allowed.
    """
    try:
        obj_name, attr = placeholder.split(".", 1)
    except ValueError as exc:
        raise ValueError(f"Invalid placeholder format: '{placeholder}'") from exc

    if obj_name == "customer":
        allowed = _allowed_customer_attrs()
        source_obj = customer
    elif obj_name == "order":
        allowed = _allowed_order_attrs()
        source_obj = order
    else:
        raise ValueError(f"Unknown placeholder object: '{obj_name}'")

    if attr not in allowed:
        raise ValueError(f"Access to restricted attribute '{attr}' is forbidden")

    return getattr(source_obj, attr)


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------


def create_order_receipt(purchase_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given purchase ID.

    Parameters
    ----------
    purchase_id : str
        Unique identifier of the order.
    receipt_template : str
        Template string containing placeholders like '{customer.name}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID does not exist or a placeholder requests restricted data.
    """
    # Retrieve the order; raise if it doesn't exist
    order = Order.get_by_id(purchase_id)
    if order is None:
        raise ValueError(f"Order with ID '{purchase_id}' does not exist")

    # Retrieve the associated customer
    # In a real system, this would be a database query.
    # For the purposes of this example we keep it simple.
    customer = CUSTOMER_REGISTRY.get(order.customer_id)
    if customer is None:
        raise ValueError(f"Customer with ID '{order.customer_id}' does not exist")

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"{([^}]+)}")
    placeholders = placeholder_pattern.findall(receipt_template)

    # Build a mapping for format_map
    mapping: Dict[str, Any] = {}
    for ph in placeholders:
        if ph not in mapping:  # avoid repeated resolution
            value = _resolve_placeholder(ph, order, customer)
            mapping[ph] = str(value)

    try:
        formatted_receipt = receipt_template.format_map(mapping)
    except KeyError as exc:
        # This should not happen because we resolved all placeholders
        raise ValueError(f"Missing placeholder during formatting: {exc}") from exc

    return formatted_receipt


# ----------------------------------------------------------------------
# Example data (for demonstration purposes)
# ----------------------------------------------------------------------


CUSTOMER_REGISTRY: Dict[str, Customer] = {}

def _setup_demo_data():
    """Populate mock registries with sample data."""
    cust = Customer(
        id="cust-001",
        name="Jane Doe",
        email="jane.doe@example.com",
        address="123 Elm Street, Springfield",
    )
    CUSTOMER_REGISTRY[cust.id] = cust

    order = Order(
        id="order-123",
        total=149.99,
        date="2024-07-22T15:30:00Z",
        items=[
            {"name": "Wireless Mouse", "price": 29.99, "qty": 2},
            {"name": "USB-C Adapter", "price": 39.99, "qty": 1},
        ],
        customer_id=cust.id,
    )
    Order.register(order)


# ----------------------------------------------------------------------
# Demo usage
# ----------------------------------------------------------------------


if __name__ == "__main__":
    _setup_demo_data()

    template = (
        "Receipt for Order #{order.id}\n"
        "Date: {order.date}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Address: {customer.address}\n"
        "Total: ${order.total:.2f}\n"
    )

    try:
        receipt = create_order_receipt("order-123", template)
        print(receipt)
    except ValueError as e:
        print(f"Error generating receipt: {e}")