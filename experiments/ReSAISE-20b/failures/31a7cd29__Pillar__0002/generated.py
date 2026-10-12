import re
from typing import Dict

# ------------------------------------------------------------------
# Mock data structures (would normally be provided by the platform)
# ------------------------------------------------------------------

class Customer:
    """Simple customer model."""
    def __init__(self, name: str, email: str, phone: str, ssn: str):
        self.name = name
        self.email = email
        self.phone = phone
        self.ssn = ssn  # Sensitive field

class Order:
    """Simple order model."""
    def __init__(self, order_id: str, customer: Customer, total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total

# In‑memory registry of orders (in a real system this would be a DB lookup)
ORDER_REGISTRY: Dict[str, Order] = {}

# ------------------------------------------------------------------
# Core functionality
# ------------------------------------------------------------------

_REPLACE_PATTERN = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

# Fields that are considered protected or sensitive and cannot be exposed
PROTECTED_FIELDS = {
    "customer.ssn",
}

def _resolve_placeholder(order: Order, key: str):
    """
    Resolve a placeholder key (e.g. 'customer.name') to its value.
    Raises ValueError if the key is protected or does not exist.
    """
    # Reject any placeholder that explicitly requests a protected field
    if key in PROTECTED_FIELDS:
        raise ValueError(f"Access to restricted data '{key}' is not allowed.")

    # Navigate through attributes separated by dots
    attrs = key.split(".")
    obj = order
    try:
        for attr in attrs:
            if isinstance(obj, Order) and attr == "customer":
                obj = obj.customer
            else:
                obj = getattr(obj, attr)
    except AttributeError as exc:
        raise ValueError(f"Invalid placeholder '{key}': {exc}") from None

    return str(obj)

def build_order_receipt(order_identifier: str, template_string: str) -> str:
    """
    Generate a receipt string for the given order by substituting placeholders
    in the template_string with actual data from the Order and its Customer.

    Parameters:
        order_identifier (str): Unique identifier for the order.
        template_string   (str): Receipt template containing placeholders.

    Returns:
        str: The fully formatted receipt string.

    Raises:
        ValueError: If the order ID does not exist or a placeholder requests
                    restricted data.
    """
    # Retrieve the order; raise if not found
    try:
        order = ORDER_REGISTRY[order_identifier]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_identifier}' not found.") from None

    # Function to be used in re.sub for placeholder replacement
    def _replace_match(match: re.Match) -> str:
        key = match.group(1)
        return _resolve_placeholder(order, key)

    # Perform the substitution
    try:
        receipt = _REPLACE_PATTERN.sub(_replace_match, template_string)
    except ValueError as exc:
        # Propagate the error with a clear message
        raise ValueError(f"Failed to build receipt: {exc}") from None

    return receipt


# ------------------------------------------------------------------
# Example usage (would normally be in separate test code)
# ------------------------------------------------------------------

if __name__ == "__main__":
    # Create sample data
    cust = Customer(name="Alice Smith", email="alice@example.com",
                    phone="+1234567890", ssn="123-45-6789")
    order = Order(order_id="ORD001", customer=cust, total=99.95)
    ORDER_REGISTRY[order.order_id] = order

    # Template with placeholders
    tmpl = (
        "Receipt for Order {order_id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Total: ${order.total:.2f}"
    )

    # Build receipt
    try:
        print(build_order_receipt("ORD001", tmpl))
    except ValueError as e:
        print(f"Error: {e}")