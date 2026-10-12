import re
from typing import Any

# ------------------------------------------------------------
# Mock data structures (replace with real implementations)
# ------------------------------------------------------------

class Customer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class Order:
    def __init__(self, order_id: str, customer: Customer, total: float, items: list):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items

# In a real system, this would query a database or external service.
ORDERS_DB = {
    "123": Order("123", Customer("Alice Smith", "alice@example.com"), 59.99, ["Book", "Pen"]),
    # Add more orders as needed
}

def get_order_by_id(order_id: str) -> Order:
    """Retrieve an Order instance by its ID."""
    order = ORDERS_DB.get(order_id)
    if not order:
        raise ValueError(f"Order ID '{order_id}' does not exist.")
    return order

# ------------------------------------------------------------
# Receipt generation logic
# ------------------------------------------------------------

PLACEHOLDER_PATTERN = re.compile(r"\{([^{}]+)\}")

def _resolve_placeholder(order: Order, placeholder: str) -> Any:
    """
    Resolve a single placeholder against an Order instance.

    The placeholder is dot-separated (e.g., 'customer.name').
    Protected attributes (starting with '_') are forbidden.
    """
    parts = placeholder.split(".")
    obj: Any = order
    for part in parts:
        if part.startswith("_"):
            raise ValueError(f"Access to protected attribute '{part}' is not allowed.")
        if not hasattr(obj, part):
            raise ValueError(f"Attribute '{part}' not found in object of type {type(obj).__name__}.")
        obj = getattr(obj, part)
    return obj

def create_purchase_receipt(order_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt string for the given order.

    Parameters
    ----------
    order_id : str
        Identifier of the order to generate a receipt for.
    receipt_template : str
        Template string containing placeholders like '{customer.name}' or '{order.total}'.

    Returns
    -------
    str
        The receipt string with placeholders replaced by actual values.

    Raises
    ------
    ValueError
        If the order ID is invalid, a placeholder refers to a protected attribute,
        or an attribute in the placeholder chain does not exist.
    """
    order = get_order_by_id(order_id)

    def _replacement(match: re.Match) -> str:
        placeholder = match.group(1).strip()
        value = _resolve_placeholder(order, placeholder)
        return str(value)

    try:
        receipt = PLACEHOLDER_PATTERN.sub(_replacement, receipt_template)
    except ValueError as exc:
        raise ValueError(f"Failed to generate receipt: {exc}") from None

    return receipt