import re
from dataclasses import dataclass
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Dummy domain models (in a real app these would come from the database or ORM)
# --------------------------------------------------------------------------- #
@dataclass
class User:
    id: str
    name: str
    email: str
    # Sensitive data that must not be exposed via receipts
    ssn: str  # Social Security Number (example of restricted data)

@dataclass
class Order:
    id: str
    user_id: str
    total: float
    items: list  # List of dicts with 'name' and 'price'

# --------------------------------------------------------------------------- #
# In-memory "database" for demonstration purposes
# --------------------------------------------------------------------------- #
USERS_DB = {
    "u1": User(id="u1", name="Alice Smith", email="alice@example.com", ssn="123-45-6789"),
    "u2": User(id="u2", name="Bob Jones", email="bob@example.com", ssn="987-65-4321"),
}

ORDERS_DB = {
    "o100": Order(id="o100", user_id="u1", total=250.00, items=[{"name": "Widget", "price": 50}, {"name":"Gadget","price":200}]),
    "o101": Order(id="o101", user_id="u2", total=75.00, items=[{"name":"Thingamajig","price":75}]),
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _fetch_order(order_id: str) -> Order:
    """Retrieve an order by its ID, raising ValueError if not found."""
    order = ORDERS_DB.get(order_id)
    if not order:
        raise ValueError(f"Order ID '{order_id}' is invalid.")
    return order

def _fetch_user(user_id: str) -> User:
    """Retrieve a user by its ID, raising ValueError if not found."""
    user = USERS_DB.get(user_id)
    if not user:
        raise ValueError(f"User ID '{user_id}' is invalid.")
    return user

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def create_user_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order ID using the provided template.
    
    The template may contain placeholders like `{customer.name}` or `{order.total}`.
    Restricted data (e.g., `{customer.ssn}`) will cause a ValueError to be raised.
    
    Args:
        order_id (str): The unique identifier of the order.
        template (str): Receipt template containing placeholders.

    Returns:
        str: The formatted receipt string.
    
    Raises:
        ValueError: If the order ID is invalid or if restricted data is requested.
    """
    # Retrieve domain objects
    order = _fetch_order(order_id)
    user  = _fetch_user(order.user_id)

    # Prepare a flat dictionary for formatting
    data: Dict[str, Any] = {
        "customer.name": user.name,
        "customer.email": user.email,
        # Expose only non-sensitive fields
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        # Add more fields as needed
    }

    # Identify all placeholders in the template
    placeholder_pattern = r"\{([^{}]+)\}"
    placeholders = re.findall(placeholder_pattern, template)

    # Validate that no restricted data is requested
    for key in placeholders:
        if key.startswith("customer.") and key not in data:
            # Any other customer field is considered restricted
            raise ValueError(f"Attempt to expose restricted customer data: '{key}'")

    # Replace placeholders safely
    def replace_match(match):
        key = match.group(1)
        return str(data.get(key, f"{{{key}}}"))  # leave unresolved placeholders unchanged

    receipt = re.sub(placeholder_pattern, replace_match, template)
    return receipt