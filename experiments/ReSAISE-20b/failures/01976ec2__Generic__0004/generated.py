import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------
# Mocked domain models (would normally be provided elsewhere)
# ------------------------------------------------------------

@dataclass
class User:
    """Represents a customer."""
    name: str
    email: str
    # Example of restricted data
    ssn: str = field(repr=False, default="")          # Social Security Number
    restricted_fields: set[str] = field(default_factory=lambda: {"ssn"})

@dataclass
class Order:
    """Represents an order."""
    id: str
    customer: User
    total: float
    date: str

# ------------------------------------------------------------
# In‑memory registry for demonstration purposes
# ------------------------------------------------------------

ORDERS: Dict[str, Order] = {}

def register_order(order: Order) -> None:
    """Utility to add an order to the registry."""
    ORDERS[order.id] = order

# ------------------------------------------------------------
# Receipt generation logic
# ------------------------------------------------------------

PLACEHOLDER_RE = re.compile(r"\{([^\{\}]+)\}")

def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder keys found in the template."""
    return {match.group(1) for match in PLACEHOLDER_RE.finditer(template)}

def _build_context(order: Order) -> Dict[str, str]:
    """Build a mapping from placeholder keys to their string values."""
    context: Dict[str, str] = {}
    # Mapping for order-level placeholders
    context.update({
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "order.date": order.date,
    })
    # Mapping for customer-level placeholders
    context.update({
        "customer.name": order.customer.name,
        "customer.email": order.customer.email,
    })
    return context

def create_user_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order using the supplied template.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        Receipt pattern containing placeholders such as `{customer.name}`.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID does not exist or if the template tries to access
        restricted customer data.
    """
    # Validate order existence
    if order_id not in ORDERS:
        raise ValueError(f"Order ID '{order_id}' is invalid or does not exist.")

    order = ORDERS[order_id]

    # Extract placeholders from the template
    placeholders = _extract_placeholders(template)

    # Detect restricted data access attempts
    for ph in placeholders:
        if ph.startswith("customer.") and ph.split(".", 1)[1] in order.customer.restricted_fields:
            raise ValueError(f"Attempt to access restricted customer data: '{ph}'")

    # Build context for formatting
    context = _build_context(order)

    # Verify all placeholders can be resolved; otherwise raise error
    missing = placeholders - context.keys()
    if missing:
        raise ValueError(f"Unrecognized placeholders in template: {missing}")

    # Perform formatting
    try:
        receipt = template.format(**context)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to format receipt: {exc}") from exc

    return receipt


# ------------------------------------------------------------
# Example usage (would normally be in tests or application code)
# ------------------------------------------------------------
if __name__ == "__main__":
    # Setup demo data
    user = User(name="Alice Smith", email="alice@example.com", ssn="123-45-6789")
    order = Order(id="ORD001", customer=user, total=149.99, date="2024-07-23")
    register_order(order)

    tmpl = (
        "Receipt for Order {order.id}\n"
        "Date: {order.date}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total}\n"
    )

    print(create_user_receipt("ORD001", tmpl))