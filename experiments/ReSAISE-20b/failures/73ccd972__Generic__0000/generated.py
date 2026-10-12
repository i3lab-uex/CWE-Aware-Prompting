import re
from typing import Any, Dict

# ----------------------------------------------------------------------
# Mocked data models (for illustration only – in real use these would be
# imported from the platform's domain layer)
# ----------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str, address: str):
        self.name = name
        self.email = email  # considered protected data
        self.address = address

class Order:
    _orders: Dict[str, "Order"] = {}

    def __init__(self, order_id: str, customer: Customer,
                 total: float, items: list[str], date: str):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items
        self.date = date

        # Register the order in a simple in‑memory store
        Order._orders[order_id] = self

    @classmethod
    def get_by_id(cls, order_id: str) -> "Order":
        return cls._orders.get(order_id)


# ----------------------------------------------------------------------
# Receipt generation logic
# ----------------------------------------------------------------------
PLACEHOLDER_PATTERN = re.compile(r"{([a-zA-Z0-9_.]+)}")

# Define which customer attributes are allowed to be exposed in a receipt.
ALLOWED_CUSTOMER_FIELDS = {"name", "address"}
# Define which order attributes are allowed to be exposed.
ALLOWED_ORDER_FIELDS = {"total", "items", "date"}


def _resolve_placeholder(obj: Any, attr_path: str) -> str:
    """
    Resolve a dotted attribute path on an object and return its string
    representation. Raises ValueError if the attribute is not allowed.
    """
    parts = attr_path.split(".")
    current_obj = obj

    for i, part in enumerate(parts):
        if not hasattr(current_obj, part):
            raise ValueError(f"Unknown placeholder attribute: '{attr_path}'")

        # If we are about to access a customer attribute, enforce the whitelist
        if isinstance(current_obj, Customer):
            if part not in ALLOWED_CUSTOMER_FIELDS:
                raise ValueError(
                    f"Access to restricted customer field '{part}' is not allowed"
                )

        # If we are about to access an order attribute, enforce the whitelist
        if isinstance(current_obj, Order):
            if part not in ALLOWED_ORDER_FIELDS:
                raise ValueError(
                    f"Access to restricted order field '{part}' is not allowed"
                )

        current_obj = getattr(current_obj, part)

    return str(current_obj)


def create_order_receipt(purchase_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given order ID.

    Parameters
    ----------
    purchase_id : str
        Unique identifier of the order.
    receipt_template : str
        Template string containing placeholders like `{customer.name}` or
        `{order.total}`.

    Returns
    -------
    str
        The receipt string with all placeholders substituted.

    Raises
    ------
    ValueError
        If the order does not exist or if a placeholder requests protected data.
    """
    # Retrieve the order
    order = Order.get_by_id(purchase_id)
    if not order:
        raise ValueError(f"Order with ID '{purchase_id}' does not exist")

    # Function to replace each placeholder
    def replacer(match: re.Match) -> str:
        full_placeholder = match.group(0)
        attr_path = match.group(1)

        # Resolve the placeholder against the order object
        return _resolve_placeholder(order, attr_path)

    # Perform substitution
    try:
        receipt = PLACEHOLDER_PATTERN.sub(replacer, receipt_template)
    except ValueError as exc:
        # Re‑raise to propagate the error message
        raise

    return receipt


# ----------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Create sample data
    cust = Customer(name="Jane Doe", email="jane@example.com", address="123 Main St")
    Order(
        order_id="ORD001",
        customer=cust,
        total=199.99,
        items=["Widget A", "Widget B"],
        date="2024-07-23"
    )

    template = (
        "Receipt for Order {order.order_id}\n"
        "Customer: {customer.name}\n"
        "Address: {customer.address}\n"
        "Date: {order.date}\n"
        "Items: {order.items}\n"
        "Total: ${order.total}"
    )

    print(create_order_receipt("ORD001", template))