import re
from typing import Dict

# ----------------------------------------------------------------------
# Mock domain models (in a real system these would be imported)
# ----------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email          # public attribute
        self._ssn = "123-45-6789"   # protected / sensitive

class Order:
    def __init__(self, order_id: str, customer: Customer, total: float, items: Dict[str, int]):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items          # dict of item_name -> quantity

# ----------------------------------------------------------------------
# In‑memory "database" of orders for demonstration purposes
# ----------------------------------------------------------------------
ORDERS_DB: Dict[str, Order] = {}

def add_order(order: Order) -> None:
    ORDERS_DB[order.order_id] = order

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def _is_protected(attr_name: str) -> bool:
    """Return True if attribute name starts with an underscore."""
    return attr_name.startswith('_')

def _get_attr_value(obj, attr_path: str):
    """
    Resolve a dotted attribute path on an object.
    Raises ValueError if any part of the path is protected or does not exist.
    """
    parts = attr_path.split('.')
    current_obj = obj
    for part in parts:
        if _is_protected(part):
            raise ValueError(f"Attempt to access protected attribute '{part}'")
        if not hasattr(current_obj, part):
            raise ValueError(f"Attribute '{part}' not found on {type(current_obj).__name__}")
        current_obj = getattr(current_obj, part)
    return current_obj

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_transaction_receipt(transaction_id: str, temp_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the provided
    template. Placeholders in the form '{customer.name}' or '{order.total}'
    are replaced with corresponding values from the Order and Customer objects.

    Args:
        transaction_id (str): The identifier of the order.
        temp_format (str): The receipt template containing placeholders.

    Returns:
        str: A fully rendered receipt string.

    Raises:
        ValueError: If the order ID is invalid or a protected attribute is accessed.
    """
    # Retrieve the order; raise if not found
    order = ORDERS_DB.get(transaction_id)
    if order is None:
        raise ValueError(f"Invalid transaction ID: {transaction_id}")

    # Regex to find placeholders like {customer.name} or {order.total}
    placeholder_pattern = re.compile(r'\{([a-zA-Z_][\w\.]*)\}')

    def replace_match(match):
        placeholder = match.group(1)          # e.g., 'customer.name'
        try:
            if placeholder.startswith('customer.'):
                value = _get_attr_value(order.customer, placeholder[len('customer.') :])
            elif placeholder.startswith('order.'):
                value = _get_attr_value(order, placeholder[len('order.') :])
            else:
                raise ValueError(f"Unsupported placeholder: {placeholder}")
        except ValueError as exc:
            # Re‑raise with context
            raise ValueError(f"Error rendering placeholder '{placeholder}': {exc}") from exc

        # Convert value to string for insertion
        return str(value)

    try:
        receipt = placeholder_pattern.sub(replace_match, temp_format)
    except ValueError as e:
        # Propagate the error
        raise

    return receipt

# ----------------------------------------------------------------------
# Example usage (for testing purposes only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    cust = Customer(name="Alice Smith", email="alice@example.com", phone="555-1234")
    order = Order(order_id="ORD001", customer=cust, total=149.99,
                  items={"Widget": 2, "Gadget": 1})
    add_order(order)

    template = (
        "Order Receipt\n"
        "==============\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Total: ${order.total:.2f}\n"
    )

    print(create_transaction_receipt("ORD001", template))