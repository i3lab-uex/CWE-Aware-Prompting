# ──────────────────────────────────────────────────────────────── #
#  Receipt generation utility for an e-commerce platform
# ──────────────────────────────────────────────────────────────── #

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any


# ------------------------------------------------------------------ #
#  Mocked domain classes – in a real system these would be imported
# ------------------------------------------------------------------ #

@dataclass
class Customer:
    id: str
    name: str
    email: str
    # Protected attribute – should not be exposed in receipts
    _ssn: str | None = field(default=None, repr=False)


@dataclass
class Order:
    id: str
    customer: Customer
    total: float
    items: list[str]


# ------------------------------------------------------------------ #
#  In‑memory repository for demo purposes
# ------------------------------------------------------------------ #

ORDERS_DB: Dict[str, Order] = {}
CUSTOMERS_DB: Dict[str, Customer] = {}


def _register_demo_data() -> None:
    """Populate the in‑memory databases with a couple of records."""
    c1 = Customer(id="c001", name="Alice Smith", email="alice@example.com")
    c2 = Customer(id="c002", name="Bob Jones", email="bob@example.com", _ssn="123-45-6789")
    o1 = Order(id="o100", customer=c1, total=199.99, items=["Widget A", "Gadget B"])
    o2 = Order(id="o101", customer=c2, total=49.95, items=["Gizmo C"])
    CUSTOMERS_DB[c1.id] = c1
    CUSTOMERS_DB[c2.id] = c2
    ORDERS_DB[o1.id] = o1
    ORDERS_DB[o2.id] = o2


_register_demo_data()


# ------------------------------------------------------------------ #
#  Utility functions
# ------------------------------------------------------------------ #

def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    pattern = r"{([a-zA-Z0-9_.]+)}"
    return set(re.findall(pattern, template))


def _build_context(order: Order) -> Dict[str, Any]:
    """Build a context dictionary for str.format() from an order."""
    ctx: Dict[str, Any] = {
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "order.items": ", ".join(order.items),
    }

    # Customer fields
    cust = order.customer
    ctx.update({
        "customer.id": cust.id,
        "customer.name": cust.name,
        "customer.email": cust.email,
    })

    # Protect access to private/protected attributes
    if hasattr(cust, "_ssn"):
        raise ValueError("Attempt to expose protected customer information")

    return ctx


# ------------------------------------------------------------------ #
#  Public API
# ------------------------------------------------------------------ #

def create_purchase_receipt(order_id: str, receipt_template: str) -> str:
    """
    Generate a formatted purchase receipt for the given order ID.

    Parameters
    ----------
    order_id : str
        Identifier of the order to be processed.
    receipt_template : str
        A template string containing placeholders such as '{customer.name}'
        or '{order.total}'. Placeholders are replaced with the relevant
        order/customer data.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if the template attempts to access
        protected customer information.
    """
    # Validate input types
    if not isinstance(order_id, str):
        raise ValueError("order_id must be a string")
    if not isinstance(receipt_template, str):
        raise ValueError("receipt_template must be a string")

    # Retrieve the order
    order = ORDERS_DB.get(order_id)
    if not order:
        raise ValueError(f"Invalid order ID: {order_id}")

    # Build the context for formatting
    context = _build_context(order)

    # Detect any placeholder that refers to a protected attribute
    placeholders = _extract_placeholders(receipt_template)
    for ph in placeholders:
        if ph.startswith("customer._"):
            raise ValueError(f"Attempt to access protected customer attribute: {ph}")

    try:
        receipt = receipt_template.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in template: {exc}") from None

    return receipt


# ------------------------------------------------------------------ #
#  Example usage (uncomment to test)
# ------------------------------------------------------------------ #

# if __name__ == "__main__":
#     tmpl = (
#         "Receipt for Order {order.id}\n"
#         "Customer: {customer.name} ({customer.email})\n"
#         "Items: {order.items}\n"
#         "Total: ${order.total}"
#     )
#     print(create_purchase_receipt("o100", tmpl))