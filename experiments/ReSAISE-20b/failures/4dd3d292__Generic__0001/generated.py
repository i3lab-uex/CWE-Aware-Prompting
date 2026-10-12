import re
from typing import Dict

# --------------------------------------------------------------------------- #
# Mock data store – in a real system this would be replaced by database access
# --------------------------------------------------------------------------- #
class Customer:
    def __init__(self, customer_id: str, name: str, email: str):
        self.customer_id = customer_id
        self.name = name          # public field
        self.email = email        # public field

class Order:
    def __init__(self, order_id: str, customer: Customer, total: float, items: list):
        self.order_id = order_id
        self.customer = customer  # reference to Customer instance
        self.total = total
        self.items = items

# Example data – replace with real persistence layer in production
_CUSTOMERS: Dict[str, Customer] = {
    "cust_001": Customer("cust_001", "Alice Smith", "alice@example.com"),
    "cust_002": Customer("cust_002", "Bob Jones", "bob@example.com"),
}

_ORDERS: Dict[str, Order] = {
    "order_1001": Order("order_1001", _CUSTOMERS["cust_001"], 59.99, ["Book A", "Pen"]),
    "order_1002": Order("order_1002", _CUSTOMERS["cust_002"], 120.00, ["Laptop"]),
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _fetch_order(order_id: str) -> Order:
    """Retrieve an order by ID, raising ValueError if not found."""
    order = _ORDERS.get(order_id)
    if not order:
        raise ValueError(f"Order ID '{order_id}' does not exist.")
    return order

def _is_protected(field_name: str) -> bool:
    """
    Determine if a field is considered protected.
    For this example, any attribute starting with an underscore is protected.
    """
    return field_name.startswith("_")

def _resolve_placeholder(order: Order, placeholder: str) -> str:
    """
    Resolve a single placeholder against the order and its related customer.
    Supports dot notation e.g. 'customer.name'.
    Raises ValueError if the field is protected or does not exist.
    """
    parts = placeholder.split(".")
    current_obj = order
    for part in parts:
        if _is_protected(part):
            raise ValueError(f"Attempted to access protected field '{part}'.")
        if not hasattr(current_obj, part):
            raise ValueError(f"Field '{part}' not found in object of type {type(current_obj).__name__}.")
        current_obj = getattr(current_obj, part)
    # Convert the final value to string for substitution
    return str(current_obj)

def _replace_placeholders(template: str, order: Order) -> str:
    """
    Replace all placeholders in the template with actual data from the order.
    Placeholders are identified by curly braces e.g. {customer.name}.
    """
    pattern = re.compile(r"\{([^}]+)\}")

    def replacer(match):
        placeholder = match.group(1).strip()
        return _resolve_placeholder(order, placeholder)

    return pattern.sub(replacer, template)


# --------------------------------------------------------------------------- #
# Main API function
# --------------------------------------------------------------------------- #

def create_purchase_receipt(order_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given order ID using the provided template.

    Args:
        order_id (str): Identifier of the order.
        receipt_template (str): Template string containing placeholders.

    Returns:
        str: The formatted receipt with all placeholders replaced.

    Raises:
        ValueError: If the order ID is invalid or if a protected field is accessed.
    """
    # Retrieve order (will raise ValueError if not found)
    order = _fetch_order(order_id)

    # Replace placeholders in the template
    receipt = _replace_placeholders(receipt_template, order)

    return receipt

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     template = (
#         "Receipt for Order {order_id}\n"
#         "Customer: {customer.name} ({customer.email})\n"
#         "Items: {items}\n"
#         "Total: ${order.total:.2f}"
#     )
#     print(create_purchase_receipt("order_1001", template))