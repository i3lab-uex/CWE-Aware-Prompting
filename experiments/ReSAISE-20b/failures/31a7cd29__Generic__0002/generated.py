import re
from dataclasses import dataclass, field
from typing import Dict, Any

# --------------------------------------------------------------------------- #
#   Mock data structures (would normally be provided by the platform)
# --------------------------------------------------------------------------- #

@dataclass
class Customer:
    name: str
    email: str
    phone: str
    address: str

@dataclass
class Order:
    id: str
    customer: Customer
    items: list[Dict[str, Any]]
    total: float

# --------------------------------------------------------------------------- #
#   In‑memory order registry (simulating a database lookup)
# --------------------------------------------------------------------------- #

ORDERS: Dict[str, Order] = {}

def register_order(order: Order) -> None:
    """Utility to add an order to the in‑memory registry."""
    ORDERS[order.id] = order

# --------------------------------------------------------------------------- #
#   Receipt generation logic
# --------------------------------------------------------------------------- #

PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")

# Fields that are considered protected and must not be exposed in a receipt
PROTECTED_FIELDS = {"email", "phone"}

def _resolve_placeholder(path: str, order: Order) -> Any:
    """
    Resolve a dotted path like 'customer.name' or 'order.total'
    against the given order object.
    """
    parts = path.split(".")
    if not parts:
        raise ValueError(f"Empty placeholder")

    # The first part must be either 'customer' or 'order'
    if parts[0] == "customer":
        obj = order.customer
        attr_path = parts[1:]
    elif parts[0] == "order":
        obj = order
        attr_path = parts[1:]
    else:
        raise ValueError(f"Unsupported placeholder root: {parts[0]}")

    # Guard against protected fields
    if attr_path and attr_path[0] in PROTECTED_FIELDS:
        raise ValueError(f"Access to protected field '{attr_path[0]}' is not allowed")

    # Walk the attribute chain
    for attr in attr_path:
        if hasattr(obj, attr):
            obj = getattr(obj, attr)
        else:
            raise ValueError(f"Attribute '{attr}' not found in {obj!r}")

    return obj

def build_order_receipt(order_identifier: str, template_string: str) -> str:
    """
    Generate a receipt by substituting placeholders in the template
    with data from the order and its customer.

    Parameters:
        order_identifier (str): The unique identifier of the order.
        template_string   (str): Receipt template containing placeholders.

    Returns:
        str: The fully formatted receipt string.

    Raises:
        ValueError: If the order ID is unknown, a placeholder is invalid,
                    or attempts to access protected data.
    """
    # Fetch the order; raise if missing
    order = ORDERS.get(order_identifier)
    if not order:
        raise ValueError(f"Order with ID '{order_identifier}' does not exist")

    # Find all placeholders in the template
    def replacement(match: re.Match) -> str:
        placeholder = match.group(1).strip()
        value = _resolve_placeholder(placeholder, order)
        # Convert non-string values to string
        return str(value)

    try:
        receipt = PLACEHOLDER_RE.sub(replacement, template_string)
    except ValueError as exc:
        # Re‑raise with a clear message
        raise ValueError(f"Failed to build receipt: {exc}") from None

    return receipt

# --------------------------------------------------------------------------- #
#   Example usage (would normally be in tests or application code)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Create a sample order
    cust = Customer(
        name="Alice Smith",
        email="alice@example.com",
        phone="+1234567890",
        address="42 Maple Street, Springfield"
    )
    order = Order(
        id="ORD12345",
        customer=cust,
        items=[{"product": "Widget", "qty": 2, "price": 19.99}],
        total=39.98
    )
    register_order(order)

    # Define a receipt template
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name}\n"
        "Address: {customer.address}\n"
        "Total: ${order.total:.2f}"
    )

    # Build the receipt
    print(build_order_receipt("ORD12345", tmpl))