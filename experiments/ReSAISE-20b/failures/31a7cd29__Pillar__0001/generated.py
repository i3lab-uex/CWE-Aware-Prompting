import re
from dataclasses import dataclass, field
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mocked data model – in a real system these would be ORM models
# ----------------------------------------------------------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str
    address: str
    ssn: str  # Restricted / protected data


@dataclass
class Order:
    id: str
    customer: Customer
    total: float
    items: list = field(default_factory=list)


# ----------------------------------------------------------------------
# In‑memory "database" of orders for demonstration purposes
# ----------------------------------------------------------------------
ORDERS_DB: Dict[str, Order] = {}


def register_order(order: Order) -> None:
    """Utility to add an order to the in‑memory DB."""
    ORDERS_DB[order.id] = order


# ----------------------------------------------------------------------
# Receipt builder
# ----------------------------------------------------------------------
class RestrictedFieldError(ValueError):
    """Raised when a placeholder refers to protected data."""


def _resolve_placeholder(match: re.Match, context: Dict[str, Any]) -> str:
    """
    Resolve a single placeholder. Raises RestrictedFieldError if the field is
    not allowed to be exposed.
    """
    path = match.group(1).strip()
    parts = path.split(".")

    # The first part must be either 'customer' or 'order'
    if not parts:
        raise ValueError(f"Empty placeholder in template")

    root = parts[0]
    if root not in ("customer", "order"):
        raise ValueError(f"Unknown placeholder root: {root}")

    # Build the nested lookup
    obj = context[root]
    for attr in parts[1:]:
        if not hasattr(obj, attr):
            raise ValueError(f"Attribute '{attr}' not found on {root}")
        obj = getattr(obj, attr)

    # Protect restricted fields
    if root == "customer" and parts[1] in {"ssn"}:
        raise RestrictedFieldError(
            f"Access to restricted field '{path}' is not allowed"
        )

    return str(obj)


def build_order_receipt(order_identifier: str, template_string: str) -> str:
    """
    Generate a receipt for the given order by substituting placeholders in
    `template_string` with actual data.

    Placeholders follow the format `{path}`, where path is a dot‑separated
    attribute chain beginning with either `customer` or `order`.

    Raises:
        ValueError: If the order does not exist, if a placeholder references
                    an unknown attribute, or if it requests restricted data.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve the order – this is our "resource" that must be
    #    properly controlled (opened and closed). In this in‑memory example,
    #    we simply fetch the object; no external resource is involved.
    # ------------------------------------------------------------------
    order = ORDERS_DB.get(order_identifier)
    if not order:
        raise ValueError(f"Order ID '{order_identifier}' does not exist")

    # ------------------------------------------------------------------
    # 2. Prepare context for placeholder resolution
    # ------------------------------------------------------------------
    context = {
        "customer": order.customer,
        "order": order,
    }

    # ------------------------------------------------------------------
    # 3. Find and replace all placeholders
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")

    try:
        result = placeholder_pattern.sub(
            lambda m: _resolve_placeholder(m, context), template_string
        )
    except RestrictedFieldError as exc:
        raise ValueError(str(exc)) from None

    return result


# ----------------------------------------------------------------------
# Example usage
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Create sample data
    cust = Customer(
        id="c123",
        name="Alice Smith",
        email="alice@example.com",
        address="123 Maple Street",
        ssn="987-65-4320",  # This should not be exposed
    )
    order = Order(
        id="o456",
        customer=cust,
        total=149.99,
        items=[
            {"name": "Widget A", "price": 49.99},
            {"name": "Widget B", "price": 100.00},
        ],
    )
    register_order(order)

    # Define a template
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Address: {customer.address}\n"
        "Total: ${order.total:.2f}"
    )

    # Build receipt
    try:
        receipt = build_order_receipt("o456", tmpl)
        print(receipt)
    except ValueError as e:
        print(f"Error generating receipt: {e}")