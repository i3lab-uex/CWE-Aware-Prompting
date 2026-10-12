import re
from dataclasses import dataclass, field
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mock data structures (in a real system these would interface with DBs)
# ----------------------------------------------------------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str  # This is considered restricted data
    phone: str

@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: list = field(default_factory=list)

# Global registries simulating persistence
CUSTOMERS: Dict[str, Customer] = {}
ORDERS: Dict[str, Order] = {}

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
_RE_PLACEHOLDER = re.compile(r'\{([a-zA-Z_][\w\.]*)\}')

def _get_attribute(obj: Any, attr_path: str) -> Any:
    """
    Resolve a dotted attribute path on an object.
    Raises AttributeError if any part of the path is missing.
    """
    parts = attr_path.split('.')
    value = obj
    for part in parts:
        if not hasattr(value, part):
            raise AttributeError(f"Attribute '{part}' not found on {value!r}")
        value = getattr(value, part)
    return value

def _is_restricted(attr_path: str) -> bool:
    """
    Determine if the attribute path refers to restricted data.
    For this example, any attribute whose name starts with '_' or
    is 'email' is considered restricted.
    """
    parts = attr_path.split('.')
    # Only check the final attribute part
    last = parts[-1]
    return last.startswith('_') or last.lower() == 'email'

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def create_receipt_for_transaction(transaction_id: str, template_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID by replacing
    placeholders in the template_format with data from the Order and its
    associated Customer.

    Raises:
        ValueError: If the transaction_id is unknown or a placeholder
                    refers to restricted data.
    """
    # Retrieve order
    if transaction_id not in ORDERS:
        raise ValueError(f"Transaction ID '{transaction_id}' does not exist.")
    order = ORDERS[transaction_id]

    # Retrieve customer
    if order.customer_id not in CUSTOMERS:
        raise ValueError(f"Customer ID '{order.customer_id}' for transaction "
                         f"'{transaction_id}' does not exist.")
    customer = CUSTOMERS[order.customer_id]

    # Function to replace each placeholder
    def _replace(match: re.Match) -> str:
        path = match.group(1).strip()
        if _is_restricted(path):
            raise ValueError(f"Restricted data requested: '{path}'")
        try:
            if path.startswith('customer.'):
                value = _get_attribute(customer, path[len('customer.') :])
            elif path.startswith('order.'):
                value = _get_attribute(order, path[len('order.') :])
            else:
                raise ValueError(f"Unknown placeholder prefix in '{path}'")
        except AttributeError as exc:
            raise ValueError(f"Invalid placeholder '{path}': {exc}") from None
        return str(value)

    # Perform substitution
    try:
        receipt = _RE_PLACEHOLDER.sub(_replace, template_format)
    except ValueError as exc:
        # Re-raise with context
        raise ValueError(str(exc)) from None

    return receipt

# ----------------------------------------------------------------------
# Example usage (for testing purposes only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Setup mock data
    c1 = Customer(id="c001", name="Alice Smith", email="alice@example.com", phone="555-0101")
    o1 = Order(id="o100", customer_id="c001", total=99.95,
               items=[{"name": "Widget", "qty": 2, "price": 19.99},
                      {"name": "Gadget", "qty": 1, "price": 59.97}])
    CUSTOMERS[c1.id] = c1
    ORDERS[o1.id] = o1

    template = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name}\n"
        "Total: ${order.total:.2f}\n"
        "Thank you for shopping with us!"
    )
    print(create_receipt_for_transaction("o100", template))