import re
from typing import Any, Dict

# ----------------------------------------------------------------------
# Mocked data structures (for illustration only; the real system will
# provide actual implementations of Order and Customer).
# ----------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str, address: str,
                 phone: str, ssn: str, credit_card: str):
        self.name = name
        self.email = email
        self.address = address
        self.phone = phone
        # Sensitive fields that must never be exposed through a receipt
        self._ssn = ssn
        self._credit_card = credit_card

class Order:
    def __init__(self, order_id: str, customer: Customer,
                 total: float, items: list):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items

# ----------------------------------------------------------------------
# Global registry of orders (simulating a database lookup).
# In production, this would be replaced by a proper persistence layer.
# ----------------------------------------------------------------------
ORDERS: Dict[str, Order] = {}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_attribute_safe(obj: Any, attr_path: str) -> Any:
    """
    Safely traverse an attribute path (e.g., 'customer.name') on `obj`.
    Raises AttributeError if any part of the path does not exist.
    """
    parts = attr_path.split('.')
    for part in parts:
        if not hasattr(obj, part):
            raise AttributeError(f"Attribute '{part}' not found.")
        obj = getattr(obj, part)
    return obj

def _is_restricted_placeholder(placeholder: str) -> bool:
    """
    Determine whether a placeholder references restricted data.
    Currently, any attribute that starts with '_' is considered protected.
    """
    # Example: '{customer._ssn}' or '{customer._credit_card}'
    return placeholder.startswith('_')

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_order_receipt(purchase_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given purchase ID using the
    provided template. The template may contain placeholders such as
    '{customer.name}' and '{order.total}'. Restricted data (attributes
    starting with an underscore) cannot be used in placeholders.

    Parameters:
        purchase_id (str): Unique identifier of the order.
        receipt_template (str): Template string containing placeholders.

    Returns:
        str: The formatted receipt with all placeholders replaced.

    Raises:
        ValueError: If the order ID does not exist or if a restricted
                    placeholder is requested.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve the order from the registry
    # ------------------------------------------------------------------
    if purchase_id not in ORDERS:
        raise ValueError(f"Order ID '{purchase_id}' does not exist.")

    order = ORDERS[purchase_id]

    # ------------------------------------------------------------------
    # 2. Identify placeholders in the template
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r'\{([^}]+)\}')
    placeholders = placeholder_pattern.findall(receipt_template)

    # ------------------------------------------------------------------
    # 3. Resolve each placeholder safely
    # ------------------------------------------------------------------
    resolved_values: Dict[str, str] = {}
    for ph in placeholders:
        # Reject any placeholder that accesses protected data
        if _is_restricted_placeholder(ph):
            raise ValueError(f"Access to restricted data '{ph}' is not allowed.")

        # Resolve the placeholder relative to the order object
        try:
            value = _get_attribute_safe(order, ph)
        except AttributeError as exc:
            raise ValueError(f"Invalid placeholder '{ph}': {exc}") from None

        # Convert non-string values to string for interpolation
        resolved_values[ph] = str(value)

    # ------------------------------------------------------------------
    # 4. Perform the substitution
    # ------------------------------------------------------------------
    def replacer(match: re.Match) -> str:
        key = match.group(1)
        return resolved_values.get(key, match.group(0))

    receipt = placeholder_pattern.sub(replacer, receipt_template)

    return receipt

# ----------------------------------------------------------------------
# Example usage (for testing purposes only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Create a sample customer and order
    cust = Customer(
        name="Jane Doe",
        email="jane@example.com",
        address="123 Main St, Anytown",
        phone="555-1234",
        ssn="123-45-6789",
        credit_card="4111 1111 1111 1111"
    )
    order = Order(
        order_id="ORD-001",
        customer=cust,
        total=149.99,
        items=["Widget A", "Gadget B"]
    )
    ORDERS[order.order_id] = order

    template = (
        "Receipt for Order {order_id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Total: ${order.total}\n"
    )

    print(create_order_receipt("ORD-001", template))