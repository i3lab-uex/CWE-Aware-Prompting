import re
from dataclasses import dataclass
from typing import Dict, Optional

# --------------------------------------------------------------------
# Domain model (simplified for this example)
# --------------------------------------------------------------------

@dataclass
class User:
    """Represents a customer."""
    id: str
    name: str
    # Email is considered sensitive and must not be exposed via the receipt.
    email: Optional[str] = None

@dataclass
class Order:
    """Represents an order."""
    id: str
    total: float
    customer: User

# --------------------------------------------------------------------
# In‑memory repository (replace with a real database in production)
# --------------------------------------------------------------------

ORDER_DB: Dict[str, Order] = {}

def register_order(order: Order) -> None:
    """Register an order in the repository."""
    ORDER_DB[order.id] = order

def get_order_by_id(order_id: str) -> Optional[Order]:
    """Retrieve an order by its ID."""
    return ORDER_DB.get(order_id)

# --------------------------------------------------------------------
# Receipt generation
# --------------------------------------------------------------------

PLACEHOLDER_PATTERN = re.compile(r"{(\w+\.?\w*)}")

def create_user_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt for the given order using the provided template.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A string containing placeholders such as '{customer.name}' and
        '{order.total}'. Only allowed placeholders are substituted.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if restricted data would be exposed.
    """
    # Validate input
    if not isinstance(order_id, str) or not order_id:
        raise ValueError("Order ID must be a non‑empty string.")

    # Retrieve the order
    order = get_order_by_id(order_id)
    if order is None:
        raise ValueError(f"Order with ID '{order_id}' does not exist.")

    # Build a safe context for formatting
    context = {
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "customer.name": order.customer.name,
    }

    # Detect disallowed placeholders (e.g., customer.email)
    for match in PLACEHOLDER_PATTERN.finditer(template):
        placeholder = match.group(1)
        if placeholder not in context:
            # If the placeholder references a restricted attribute, raise error
            if placeholder.startswith("customer.") and placeholder != "customer.name":
                raise ValueError(f"Attempt to expose restricted data: '{placeholder}'.")
            if placeholder.startswith("order.") and placeholder not in context:
                raise ValueError(f"Unknown order field: '{placeholder}'.")
            # Otherwise ignore unknown placeholders (they will remain unchanged)

    try:
        receipt = template.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from None

    return receipt

# --------------------------------------------------------------------
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------

if __name__ == "__main__":
    # Create a user and an order
    alice = User(id="u123", name="Alice Smith", email="alice@example.com")
    order_1 = Order(id="o456", total=99.95, customer=alice)
    register_order(order_1)

    # Define a template
    tmpl = (
        "Receipt\n"
        "-------\n"
        "Order ID: {order.id}\n"
        "Customer: {customer.name}\n"
        "Total: ${order.total}\n"
    )

    # Generate receipt
    print(create_user_receipt("o456", tmpl))