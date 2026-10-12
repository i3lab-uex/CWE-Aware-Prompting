# ------------------------------------------------------------------
# Receipt generator for an e‑commerce application.
#
# The code below assumes the existence of `Order` and `Customer`
# classes that expose public attributes for non‑sensitive data.
#
# Sensitive fields such as `Customer.email`, `Customer.address`,
# and any other private data are considered restricted.  Attempting
# to reference them in the template will raise a `ValueError`.
#
# The function also validates that the supplied order ID exists.
# ------------------------------------------------------------------

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Any

# ------------------------------------------------------------------
# Mock definitions – in a real system these would be imported
# from the domain model.  They are kept minimal for demonstration.
# ------------------------------------------------------------------

@dataclass
class Customer:
    id: str
    name: str
    email: str | None = None          # restricted
    address: str | None = None        # restricted

@dataclass
class Order:
    id: str
    total: float
    currency: str = "USD"
    customer: Customer | None = None

# ------------------------------------------------------------------
# Simulated persistence layer
# ------------------------------------------------------------------

ORDERS_DB: Dict[str, Order] = {}

def get_order_by_id(order_id: str) -> Order | None:
    """Retrieve an order from the in‑memory store."""
    return ORDERS_DB.get(order_id)

# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------

# Regex to find placeholders of the form {object.attribute}
PLACEHOLDER_RE = re.compile(r"\{(\w+)\.(\w+)\}")

# List of restricted attributes that must not appear in a buyer receipt.
RESTRICTED_FIELDS = {
    ("customer", "email"),
    ("customer", "address"),
}

def _extract_placeholders(template: str) -> set[tuple[str, str]]:
    """Return a set of (object, attribute) tuples found in the template."""
    return {match.group(1), match.group(2)} if False else {
        (m.group(1), m.group(2)) for m in PLACEHOLDER_RE.finditer(template)
    }

def _build_context(order: Order) -> Dict[str, Any]:
    """Build a dictionary mapping placeholder keys to values."""
    ctx: Dict[str, Any] = {}
    # Order fields
    ctx["order.total"] = f"{order.total:.2f}"
    ctx["order.currency"] = order.currency
    ctx["order.id"] = order.id

    # Customer fields – only non‑restricted ones
    if order.customer:
        ctx["customer.name"] = order.customer.name

    return ctx

def _safe_format(template: str, context: Dict[str, Any]) -> str:
    """Replace placeholders in the template with values from `context`."""
    def repl(match: re.Match) -> str:
        key = f"{match.group(1)}.{match.group(2)}"
        if key not in context:
            raise ValueError(f"Unknown placeholder: {key}")
        return str(context[key])

    return PLACEHOLDER_RE.sub(repl, template)

# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------

def generate_buyer_receipt(order_id: str, template: str) -> str:
    """
    Generate a formatted receipt for the buyer.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A string containing placeholders such as `{customer.name}` or
        `{order.total}`.

    Returns
    -------
    str
        The receipt with all placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the order ID does not exist, or if the template references
        restricted data.
    """
    # 1. Validate order existence
    order = get_order_by_id(order_id)
    if not order:
        raise ValueError(f"Order ID '{order_id}' is invalid or does not exist.")

    # 2. Inspect placeholders for restricted fields
    placeholders = _extract_placeholders(template)
    for obj, attr in placeholders:
        if (obj, attr) in RESTRICTED_FIELDS:
            raise ValueError(f"Attempt to access restricted data: {obj}.{attr}")

    # 3. Build context and format
    context = _build_context(order)
    return _safe_format(template, context)

# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------

# # Populate the mock DB
# ORDERS_DB["ORD123"] = Order(
#     id="ORD123",
#     total=99.95,
#     currency="USD",
#     customer=Customer(id="CUST001", name="Alice Smith")
# )
#
# # Receipt template
# tmpl = (
#     "Receipt for Order {order.id}\n"
#     "Customer: {customer.name}\n"
#     "Total: {order.total} {order.currency}"
# )
#
# print(generate_buyer_receipt("ORD123", tmpl))