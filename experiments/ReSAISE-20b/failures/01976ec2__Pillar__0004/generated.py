import re
from dataclasses import dataclass
from typing import Dict, Any

# -------------------------------------------------------------
# Dummy data models (in a real application these would be ORM models)
# -------------------------------------------------------------

@dataclass
class User:
    id: str
    name: str
    email: str
    # Sensitive data that should not be exposed via the receipt template
    password_hash: str

@dataclass
class Order:
    id: str
    total: float
    customer: User

# -------------------------------------------------------------
# In‑memory "database" for demonstration purposes
# -------------------------------------------------------------

_USERS: Dict[str, User] = {
    "u1": User(id="u1", name="Alice Smith", email="alice@example.com", password_hash="hashed_pw_123"),
    "u2": User(id="u2", name="Bob Jones", email="bob@example.com", password_hash="hashed_pw_456"),
}

_ORDERS: Dict[str, Order] = {
    "o100": Order(id="o100", total=49.99, customer=_USERS["u1"]),
    "o101": Order(id="o101", total=19.95, customer=_USERS["u2"]),
}

# -------------------------------------------------------------
# Helper utilities
# -------------------------------------------------------------

PLACEHOLDER_REGEX = re.compile(r"{([^{}]+)}")
# Map from placeholder key to a function that returns the value
PLACEHOLDER_RESOLVERS = {
    "customer.name": lambda order: order.customer.name,
    "customer.email": lambda order: order.customer.email,
    "order.total":   lambda order: f"{order.total:.2f}",
    "order.id":      lambda order: order.id,
}

# List of forbidden attributes that should not be exposed via the template
FORBIDDEN_PLACEHOLDERS = {"customer.password_hash", "user.password_hash"}

def _resolve_placeholder(order: Order, key: str) -> Any:
    """
    Resolve a single placeholder key against the given order.
    Raises ValueError if the key is not allowed or cannot be resolved.
    """
    if key in FORBIDDEN_PLACEHOLDERS:
        raise ValueError(f"Attempt to expose restricted data: '{key}'")

    resolver = PLACEHOLDER_RESOLVERS.get(key)
    if resolver is None:
        raise ValueError(f"Unknown placeholder: '{key}'")

    return resolver(order)

# -------------------------------------------------------------
# Main function
# -------------------------------------------------------------

def create_user_receipt(order_id: str, template: str) -> str:
    """
    Generate a formatted receipt string for the given order ID and template.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A string containing placeholders such as '{customer.name}' and '{order.total}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if a placeholder refers to restricted data.
    """
    # Retrieve the order; raise an error if not found
    order = _ORDERS.get(order_id)
    if order is None:
        raise ValueError(f"Invalid order ID: '{order_id}'")

    # Find all placeholders in the template
    placeholders = PLACEHOLDER_REGEX.findall(template)

    # Build a mapping of placeholder -> resolved value
    values: Dict[str, Any] = {}
    for key in placeholders:
        if key not in values:  # Resolve each unique placeholder only once
            values[key] = _resolve_placeholder(order, key)

    # Perform the substitution safely
    try:
        receipt = template.format(**values)
    except KeyError as exc:
        # This should not happen because we resolved all placeholders,
        # but handle it just in case
        raise ValueError(f"Missing value for placeholder: {exc}") from exc

    return receipt

# -------------------------------------------------------------
# Example usage (uncomment to test)
# -------------------------------------------------------------

# if __name__ == "__main__":
#     tmpl = (
#         "Receipt for Order {order.id}\n"
#         "Customer: {customer.name} ({customer.email})\n"
#         "Total: ${order.total}"
#     )
#     print(create_user_receipt("o100", tmpl))