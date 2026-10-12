import re
from dataclasses import dataclass, field
from typing import Dict

# --- Mock data models ---------------------------------------------------------

@dataclass
class Customer:
    """Represents a customer with public and protected attributes."""
    name: str
    email: str
    address: str
    # Protected data – should never appear in a receipt
    ssn: str = field(repr=False, default="")          # Social Security Number
    password_hash: str = field(repr=False, default="")

@dataclass
class Order:
    """Represents an order with a reference to its customer."""
    id: str
    customer: Customer
    items: list[str]
    total: float

# --- Order storage ------------------------------------------------------------

# In a real system this would be replaced by database queries.
ORDER_DB: Dict[str, Order] = {}

def add_order(order: Order) -> None:
    """Utility to register an order in the mock database."""
    ORDER_DB[order.id] = order


# --- Receipt generation -------------------------------------------------------

# Set of placeholders that are considered sensitive and must not be exposed.
PROTECTED_PLACEHOLDERS = {
    "customer.ssn",
    "customer.password_hash",
    "customer.password",  # in case a placeholder is incorrectly named
}

# Regular expression to find all placeholders of the form {foo.bar}
PLACEHOLDER_RE = re.compile(r"{\s*([a-zA-Z_][a-zA-Z0-9_.]*)\s*}")

def _resolve_placeholder(key: str, order: Order) -> str:
    """
    Resolve a single placeholder key against the given order.

    Parameters
    ----------
    key : str
        The dotted path (e.g. 'customer.name' or 'order.total').
    order : Order
        The order instance.

    Returns
    -------
    str
        The string representation of the resolved value.

    Raises
    ------
    ValueError
        If the placeholder is protected or does not exist.
    """
    if key in PROTECTED_PLACEHOLDERS:
        raise ValueError(f"Access to protected data '{key}' is not allowed.")

    # Split the key into top-level and sub-attribute
    parts = key.split(".")
    if not parts:
        raise ValueError(f"Invalid placeholder '{key}'.")
    
    # Resolve the top-level object
    if parts[0] == "order":
        obj = order
    elif parts[0] == "customer":
        obj = order.customer
    else:
        raise ValueError(f"Unknown placeholder namespace '{parts[0]}' in '{key}'.")
    
    # Resolve nested attributes
    for attr in parts[1:]:
        if not hasattr(obj, attr):
            raise ValueError(f"Attribute '{attr}' not found in '{key}'.")
        obj = getattr(obj, attr)
    
    return str(obj)

def create_order_receipt(purchase_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given order.

    Parameters
    ----------
    purchase_id : str
        The unique identifier of the order.
    receipt_template : str
        A template string containing placeholders such as '{customer.name}'.

    Returns
    -------
    str
        The receipt string with placeholders replaced by actual values.

    Raises
    ------
    ValueError
        If the order ID does not exist, or if a placeholder requests restricted data.
    """
    # Retrieve the order
    order = ORDER_DB.get(purchase_id)
    if not order:
        raise ValueError(f"Order with ID '{purchase_id}' does not exist.")

    # Find all placeholders in the template
    placeholders = set(PLACEHOLDER_RE.findall(receipt_template))

    # Resolve each placeholder and build a mapping
    resolved = {}
    for key in placeholders:
        resolved[key] = _resolve_placeholder(key, order)

    # Perform the substitution
    try:
        receipt = receipt_template.format(**resolved)
    except KeyError as exc:
        raise ValueError(f"Missing value for placeholder {exc}") from None

    return receipt


# --- Example usage -------------------------------------------------------------

if __name__ == "__main__":
    # Create a sample customer and order
    cust = Customer(
        name="Alice Smith",
        email="alice@example.com",
        address="123 Maple Street, Springfield",
        ssn="123-45-6789",
        password_hash="hashed_pw"
    )
    order = Order(
        id="ORD-001",
        customer=cust,
        items=["Widget A", "Widget B"],
        total=149.99
    )
    add_order(order)

    template = (
        "Thank you for your purchase, {customer.name}!\n"
        "Order ID: {order.id}\n"
        "Total: ${order.total:.2f}\n"
        "Shipping to: {customer.address}\n"
    )

    print(create_order_receipt("ORD-001", template))