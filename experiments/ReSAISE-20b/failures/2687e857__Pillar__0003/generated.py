import re
from typing import Dict, Any

# --------------------------------------------------------------
# Stub definitions for Order and Customer. In a real system these
# would be imported from the appropriate modules.
# --------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str, address: str):
        self.name = name
        self.email = email
        self.address = address

class Order:
    _orders: Dict[str, "Order"] = {}

    def __init__(self, order_id: str, customer: Customer, total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        Order._orders[order_id] = self

    @classmethod
    def get(cls, order_id: str) -> "Order":
        return cls._orders.get(order_id)


# --------------------------------------------------------------
# Helper: safe attribute resolution
# --------------------------------------------------------------
def _resolve_attribute(obj: Any, attr_path: str) -> Any:
    """
    Resolve a dotted attribute path on an object.
    Raises ValueError if the path attempts to access protected attributes
    (starting with '_') or if an attribute is missing.
    """
    parts = attr_path.split('.')
    current: Any = obj
    for part in parts:
        if part.startswith('_'):
            raise ValueError(f"Access to protected attribute '{part}' is not allowed.")
        if not hasattr(current, part):
            raise ValueError(f"Attribute '{part}' does not exist on object of type {type(current).__name__}.")
        current = getattr(current, part)
    return current


# --------------------------------------------------------------
# Main function
# --------------------------------------------------------------
def create_transaction_receipt(transaction_id: str, temp_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the
    supplied template.

    Parameters
    ----------
    transaction_id : str
        Identifier of the order.
    temp_format : str
        Template string containing placeholders like '{customer.name}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or a protected attribute is referenced.
    """
    # Retrieve the order; raise if not found
    order = Order.get(transaction_id)
    if order is None:
        raise ValueError(f"Invalid transaction ID: {transaction_id}")

    # Prepare a mapping of placeholder names to values
    def replacement(match: re.Match) -> str:
        key = match.group(1)
        try:
            value = _resolve_attribute(order, key)
        except ValueError as exc:
            raise ValueError(f"Invalid placeholder '{{{key}}}': {exc}") from None
        return str(value)

    # Perform safe substitution using regex to avoid format() pitfalls
    placeholder_pattern = re.compile(r'\{([a-zA-Z_][\w\.]*)\}')
    receipt = placeholder_pattern.sub(replacement, temp_format)

    return receipt


# --------------------------------------------------------------
# Example usage (this would normally be in a separate test module)
# --------------------------------------------------------------
if __name__ == "__main__":
    # Setup example data
    cust = Customer(name="Alice Smith", email="alice@example.com", address="123 Maple St")
    Order(order_id="ORD001", customer=cust, total=129.99)

    template = (
        "Receipt for Order {order_id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Address: {customer.address}\n"
        "Total Amount: ${order.total:.2f}"
    )

    print(create_transaction_receipt("ORD001", template))