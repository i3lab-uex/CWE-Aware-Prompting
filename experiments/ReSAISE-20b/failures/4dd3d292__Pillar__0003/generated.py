import re
from typing import Dict

# ----------------------------------------------------------------------
# Mock data structures (in a real system these would be ORM models)
# ----------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        # Example of a protected attribute that should not be exposed
        self._ssn = "123-45-6789"

class Order:
    def __init__(self, order_id: str, customer: Customer, total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total

# ----------------------------------------------------------------------
# In‑memory “database” of orders for demo purposes
# ----------------------------------------------------------------------
ORDERS_DB: Dict[str, Order] = {}

def _register_order(order: Order) -> None:
    """Utility to add an order to the in‑memory database."""
    ORDERS_DB[order.order_id] = order

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
PLACEHOLDER_PATTERN = re.compile(r'\{([^{}]+)\}')

def create_purchase_receipt(order_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given order.

    Parameters
    ----------
    order_id : str
        Identifier of the order to generate a receipt for.
    receipt_template : str
        Template string containing placeholders like `{customer.name}` or `{order.total}`.

    Returns
    -------
    str
        The receipt string with placeholders substituted by actual values.

    Raises
    ------
    ValueError
        If the order_id does not exist or if a placeholder refers to a protected attribute.
    """
    # Retrieve the order – raise if not found
    try:
        order = ORDERS_DB[order_id]
    except KeyError as exc:
        raise ValueError(f"Invalid order ID: {order_id}") from exc

    # Helper to resolve a single placeholder
    def _resolve_placeholder(match: re.Match) -> str:
        expr = match.group(1).strip()
        # Split into object path: e.g., 'customer.name' -> ['customer', 'name']
        parts = expr.split('.')
        if not parts:
            return ""

        # Resolve the root object (order or customer)
        obj = order
        if parts[0] == 'customer':
            obj = order.customer
        elif parts[0] != 'order':
            raise ValueError(f"Unknown root object '{parts[0]}' in placeholder")

        # Walk through the remaining attributes
        for attr_name in parts[1:]:
            if attr_name.startswith('_'):
                raise ValueError(f"Access to protected attribute '{attr_name}' is not allowed")
            if not hasattr(obj, attr_name):
                raise ValueError(f"Attribute '{attr_name}' not found on {obj.__class__.__name__}")
            obj = getattr(obj, attr_name)

        # Convert the final value to string
        return str(obj)

    # Perform substitution safely
    try:
        receipt = PLACEHOLDER_PATTERN.sub(_resolve_placeholder, receipt_template)
    except ValueError as exc:
        # Re‑raise to propagate error
        raise

    return receipt


# ----------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Setup demo data
    customer = Customer(name="Alice Smith", email="alice@example.com")
    order = Order(order_id="ORD12345", customer=customer, total=149.99)
    _register_order(order)

    template = (
        "Thank you for your purchase!\n"
        "Order ID: {order.order_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total}\n"
    )

    try:
        print(create_purchase_receipt("ORD12345", template))
    except ValueError as e:
        print(f"Error: {e}")