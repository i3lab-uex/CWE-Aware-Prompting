import re
from typing import Dict

# ------------------------------------------------------------------
# Mock data structures (replace with real implementations in production)
# ------------------------------------------------------------------

class Customer:
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email
        self.phone = phone

class Order:
    def __init__(self, order_id: str, customer: Customer, total: float, items: Dict[str, int]):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items

# In a real system this would come from a database or external service
ORDERS: Dict[str, Order] = {}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

_placeholder_re = re.compile(r'\{([^{}]+)\}')

def _get_attr_safe(obj, attr_name: str):
    """
    Safely retrieve an attribute from an object.
    Raises ValueError if the attribute is protected (starts with '_')
    or does not exist.
    """
    if attr_name.startswith('_'):
        raise ValueError(f"Access to protected attribute '{attr_name}' is not allowed.")
    if not hasattr(obj, attr_name):
        raise ValueError(f"Attribute '{attr_name}' does not exist on object of type {type(obj).__name__}.")
    return getattr(obj, attr_name)

def _resolve_placeholder(match: re.Match, order: Order) -> str:
    """
    Resolve a single placeholder against an Order instance.
    Supports nested attributes via dot notation (e.g., 'customer.name').
    """
    expr = match.group(1).strip()
    parts = expr.split('.')
    current_obj = order
    for part in parts:
        current_obj = _get_attr_safe(current_obj, part)
    # Convert final value to string
    return str(current_obj)

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def create_transaction_receipt(transaction_id: str, temp_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the provided template.
    
    Args:
        transaction_id: Identifier of the order to look up.
        temp_format: Template string containing placeholders like '{customer.name}'.

    Returns:
        A formatted receipt string with all placeholders replaced by actual values.

    Raises:
        ValueError: If the transaction ID is invalid or a placeholder references
                    protected or non‑existent data.
    """
    # Validate transaction ID and retrieve order
    if not isinstance(transaction_id, str) or not transaction_id:
        raise ValueError("Transaction ID must be a non‑empty string.")
    order = ORDERS.get(transaction_id)
    if order is None:
        raise ValueError(f"Order with ID '{transaction_id}' does not exist.")

    # Replace placeholders safely
    try:
        receipt = _placeholder_re.sub(lambda m: _resolve_placeholder(m, order), temp_format)
    except ValueError as e:
        # Re‑raise to caller
        raise ValueError(f"Failed to generate receipt: {e}") from None

    return receipt