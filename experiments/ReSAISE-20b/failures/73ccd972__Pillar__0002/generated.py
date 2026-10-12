import re
from typing import Dict, Any

# --------------------------------------------------------------------
# Mock data structures (replace with real ORM models in production)
# --------------------------------------------------------------------

class Customer:
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email
        self.phone = phone
        # protected attributes that must not be exposed in receipts
        self._password = "s3cr3t"

class Order:
    def __init__(self, order_id: str, customer: Customer, total: float, items: list):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items

# In‑memory order store (replace with database access in production)
ORDER_STORE: Dict[str, Order] = {}

def add_order(order: Order):
    """Utility to register an order for the demo."""
    ORDER_STORE[order.order_id] = order

# --------------------------------------------------------------------
# Receipt generation logic
# --------------------------------------------------------------------

# Whitelist of allowed placeholder paths (dot notation)
ALLOWED_PATHS = {
    "customer.name",
    "customer.email",
    "customer.phone",
    "order.total",
    "order.items",  # will be stringified
}

# Regular expression to find placeholders like {customer.name}
PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")

def _get_value_by_path(obj: Any, path: str) -> Any:
    """Retrieve nested attribute value from an object following a dot‑separated path."""
    parts = path.split(".")
    current: Any = obj
    for part in parts:
        if not hasattr(current, part):
            raise ValueError(f"Attribute '{part}' not found in object of type {type(current).__name__}")
        current = getattr(current, part)
    return current

def create_order_receipt(purchase_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given purchase ID.

    Parameters
    ----------
    purchase_id : str
        Unique identifier of the order.
    receipt_template : str
        Template string containing placeholders such as '{customer.name}'.

    Returns
    -------
    str
        Formatted receipt with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the order does not exist or a placeholder requests disallowed data.
    """
    # ----------------------------------------------------------------
    # 1. Retrieve order (simulated DB access)
    # ----------------------------------------------------------------
    order = ORDER_STORE.get(purchase_id)
    if not order:
        raise ValueError(f"Order with ID '{purchase_id}' does not exist.")

    # ----------------------------------------------------------------
    # 2. Find and replace placeholders
    # ----------------------------------------------------------------
    def replacement(match: re.Match) -> str:
        placeholder = match.group(1).strip()
        if placeholder not in ALLOWED_PATHS:
            raise ValueError(f"Disallowed or unknown placeholder '{placeholder}'.")
        try:
            value = _get_value_by_path(order, placeholder)
        except ValueError as e:
            raise ValueError(f"Error resolving placeholder '{placeholder}': {e}")

        # Convert complex types to string safely
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        return str(value)

    try:
        receipt = PLACEHOLDER_RE.sub(replacement, receipt_template)
    except ValueError as e:
        raise

    return receipt

# --------------------------------------------------------------------
# Example usage (for demonstration; remove or comment out in production)
# --------------------------------------------------------------------

if __name__ == "__main__":
    # Setup demo data
    cust = Customer(name="Alice Smith", email="alice@example.com", phone="555-1234")
    order = Order(order_id="ORD001", customer=cust, total=149.99, items=["Book", "Pen"])
    add_order(order)

    template = (
        "Receipt for Order {order.order_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Items: {order.items}\n"
        "Total: ${order.total:.2f}"
    )

    try:
        print(create_order_receipt("ORD001", template))
    except ValueError as exc:
        print(f"Error: {exc}")