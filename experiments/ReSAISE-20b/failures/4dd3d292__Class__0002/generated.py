import re
from typing import Dict, Any

# --------------------------------------------------------------------
# Mock definitions of Order and Customer for demonstration purposes.
# In a real system these would be replaced by the actual implementations.
# --------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self._email = email          # protected field
        self.phone = phone

    @property
    def email(self) -> str:
        """Access to the customer's email is considered sensitive."""
        raise AttributeError("Access to protected attribute 'email' is denied.")


class Order:
    _orders_db: Dict[str, "Order"] = {}

    def __init__(self, order_id: str, customer: Customer, total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total

    @classmethod
    def get_by_id(cls, order_id: str) -> "Order":
        if order_id not in cls._orders_db:
            raise ValueError(f"Invalid order ID: {order_id}")
        return cls._orders_db[order_id]

    @classmethod
    def register_order(cls, order: "Order"):
        cls._orders_db[order.order_id] = order


# --------------------------------------------------------------------
# Helper function to safely resolve placeholders
# --------------------------------------------------------------------
_PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

def _resolve_placeholder(match: re.Match, context: Dict[str, Any]) -> str:
    """
    Resolve a single placeholder from the context dictionary.
    Raise ValueError if the field is not present or protected.
    """
    path = match.group(1).split(".")
    value: Any = context
    for attr in path:
        if isinstance(value, dict):
            # For nested dictionaries
            value = value.get(attr)
        else:
            try:
                # Prevent access to protected attributes (starting with underscore)
                if attr.startswith("_"):
                    raise AttributeError(f"Attempted to access protected attribute '{attr}'.")
                value = getattr(value, attr)
            except AttributeError:
                raise ValueError(f"Invalid placeholder: '{{{match.group(1)}}}'")
        if value is None:
            raise ValueError(f"Invalid placeholder: '{{{match.group(1)}}}'")
    # Convert value to string for formatting
    return str(value)


def create_purchase_receipt(order_id: str, receipt_template: str) -> str:
    """
    Generate a purchase receipt by replacing placeholders in the template
    with actual order and customer information.

    Parameters:
        order_id (str): Identifier of the order.
        receipt_template (str): Template containing placeholders like
            '{customer.name}' or '{order.total}'.

    Returns:
        str: The formatted receipt string.

    Raises:
        ValueError: If the order ID is invalid or a placeholder references
            protected or non‑existent data.
    """
    # Retrieve the order and ensure it exists
    try:
        order = Order.get_by_id(order_id)
    except ValueError as exc:
        raise ValueError(f"Order not found: {order_id}") from exc

    # Prepare context for placeholder resolution
    context = {
        "order": order,
        "customer": order.customer,
    }

    # Resolve placeholders safely
    try:
        receipt = _PLACEHOLDER_RE.sub(lambda m: _resolve_placeholder(m, context), receipt_template)
    except ValueError as exc:
        # Re‑raise with a clear message
        raise ValueError(f"Receipt generation failed: {exc}") from exc

    return receipt


# --------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------
if __name__ == "__main__":
    # Create sample data
    cust = Customer(name="Alice Smith", email="alice@example.com", phone="+1234567890")
    order = Order(order_id="ORD12345", customer=cust, total=149.99)
    Order.register_order(order)

    # Define a template
    tmpl = (
        "Receipt for order {order.order_id}\n"
        "Customer: {customer.name}\n"
        "Phone: {customer.phone}\n"
        "Total: ${order.total:.2f}"
    )

    # Generate receipt
    print(create_purchase_receipt("ORD12345", tmpl))