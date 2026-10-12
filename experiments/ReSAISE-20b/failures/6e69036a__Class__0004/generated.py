import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mock domain models (would normally be imported from the application)
# ----------------------------------------------------------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str
    phone: str
    # Sensitive fields (should not be exposed)
    ssn: str = ""  # Social Security Number
    credit_card_number: str = ""

@dataclass
class Order:
    id: str
    customer: Customer
    total: float
    date: datetime

# ----------------------------------------------------------------------
# In‑memory repository for demonstration purposes
# ----------------------------------------------------------------------
ORDERS_DB: Dict[str, Order] = {}

def add_order(order: Order) -> None:
    """Utility to seed the mock database."""
    ORDERS_DB[order.id] = order

# ----------------------------------------------------------------------
# Receipt generation
# ----------------------------------------------------------------------
ALLOWED_PLACEHOLDERS = {
    "customer.name",
    "customer.email",
    "customer.phone",
    "order.id",
    "order.total",
    "order.date",  # formatted as ISO string
}

PLACEHOLDER_PATTERN = re.compile(r"\{([^}]+)\}")

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in PLACEHOLDER_PATTERN.finditer(template)}

def _build_context(order: Order) -> Dict[str, Any]:
    """Create a context dictionary for string formatting."""
    return {
        "customer.name": order.customer.name,
        "customer.email": order.customer.email,
        "customer.phone": order.customer.phone,
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "order.date": order.date.isoformat(),
    }

def generate_client_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        Receipt template containing placeholders like '{customer.name}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order_id is invalid or the template contains disallowed placeholders.
    """
    # Validate order existence
    order = ORDERS_DB.get(order_id)
    if not order:
        raise ValueError(f"Invalid order ID: {order_id}")

    # Extract placeholders from template
    placeholders = _extract_placeholders(template)

    # Ensure no disallowed placeholder is present
    for ph in placeholders:
        if ph not in ALLOWED_PLACEHOLDERS:
            raise ValueError(
                f"Disallowed placeholder '{ph}' in template. "
                "Only the following placeholders are permitted: "
                f"{', '.join(sorted(ALLOWED_PLACEHOLDERS))}"
            )

    # Build context for formatting
    context = _build_context(order)

    try:
        receipt = template.format(**context)
    except KeyError as exc:
        # This should not happen due to prior checks, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return receipt

# ----------------------------------------------------------------------
# Example usage (for testing purposes)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Seed data
    cust = Customer(
        id="cust123",
        name="Alice Smith",
        email="alice@example.com",
        phone="+1-555-0123",
        ssn="123-45-6789",
    )
    order = Order(
        id="order456",
        customer=cust,
        total=149.99,
        date=datetime.now(),
    )
    add_order(order)

    tmpl = (
        "Receipt\n"
        "-------\n"
        "Order ID: {order.id}\n"
        "Date: {order.date}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Phone: {customer.phone}\n"
        "Total: ${order.total}\n"
    )

    print(generate_client_receipt("order456", tmpl))