import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Mocked data structures (in real life these would be provided by the
# application framework or ORM)
# ------------------------------------------------------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str  # *restricted*
    address: str


@dataclass
class Order:
    id: str
    total: float
    status: str
    customer_id: str
    # *restricted* attributes that should not appear in the receipt
    _created_at: str = field(repr=False)
    _internal_notes: str = field(repr=False)


# ------------------------------------------------------------------
# Simple in‑memory "database"
# ------------------------------------------------------------------
CUSTOMERS: Dict[str, Customer] = {
    "c1": Customer(id="c1", name="Alice Smith", email="alice@example.com",
                   address="123 Main St, Anytown"),
}

ORDERS: Dict[str, Order] = {
    "o1": Order(id="o1", total=149.99, status="shipped",
                customer_id="c1", _created_at="2023-08-01T12:34:56Z",
                _internal_notes="Priority shipping"),
}


# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------
_RE_PLACEHOLDER = re.compile(r"{([^{}]+)}")


def _get_attr(obj, attr_path: str):
    """Traverse nested attributes safely."""
    parts = attr_path.split(".")
    for part in parts:
        if not hasattr(obj, part):
            raise AttributeError(f"Attribute '{part}' not found on {obj!r}")
        obj = getattr(obj, part)
    return obj


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_receipt_for_transaction(transaction_id: str, template_format: str) -> str:
    """
    Generate a receipt string by replacing placeholders in `template_format`
    with data from the order and its associated customer.

    Raises:
        ValueError: If the transaction ID is unknown, or if a placeholder
                    references restricted data.
    """
    # 1. Retrieve the order
    if transaction_id not in ORDERS:
        raise ValueError(f"Order with ID '{transaction_id}' does not exist.")
    order = ORDERS[transaction_id]

    # 2. Retrieve the customer
    if order.customer_id not in CUSTOMERS:
        raise ValueError(f"Customer with ID '{order.customer_id}' does not exist.")
    customer = CUSTOMERS[order.customer_id]

    # 3. Build a mapping of allowed placeholders
    allowed_placeholders = {
        "order.id": order.id,
        "order.total": f"${order.total:.2f}",
        "order.status": order.status,
        "customer.id": customer.id,
        "customer.name": customer.name,
        "customer.address": customer.address,
    }

    # 4. Find all placeholders in the template
    found_placeholders = set(_RE_PLACEHOLDER.findall(template_format))

    # 5. Validate placeholders
    for ph in found_placeholders:
        if ph not in allowed_placeholders:
            # Either unknown placeholder or restricted data
            raise ValueError(f"Placeholder '{ph}' is not allowed or does not exist.")

    # 6. Perform safe formatting
    try:
        receipt = template_format.format(**allowed_placeholders)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder value for {exc}") from exc

    return receipt


# ------------------------------------------------------------------
# Example usage (for demonstration; remove or comment out in production)
# ------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Receipt for Order #{order.id}\n"
        "Customer: {customer.name}\n"
        "Address: {customer.address}\n"
        "Total Paid: {order.total}\n"
        "Status: {order.status}"
    )
    print(create_receipt_for_transaction("o1", template))