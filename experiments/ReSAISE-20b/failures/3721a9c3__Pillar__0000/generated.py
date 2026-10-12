import re
from string import Formatter

# ------------------------------------------------------------
# Dummy data store and entity definitions (for illustration only)
# In a real application these would be provided by the framework or
# a database layer.
# ------------------------------------------------------------

class Customer:
    """Represents a customer. Only certain attributes are allowed to be exposed."""
    def __init__(self, name: str, email: str, ssn: str = None):
        self.name = name
        self.email = email
        self.ssn = ssn  # Sensitive data, should not be exposed

class Order:
    """Represents an order. Contains a reference to its customer."""
    _store = {}  # simple in‑memory store keyed by order_id

    def __init__(self, order_id: str, customer: Customer, total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        Order._store[order_id] = self

    @classmethod
    def get_by_id(cls, order_id: str):
        return cls._store.get(order_id)

# ------------------------------------------------------------
# Core function
# ------------------------------------------------------------

def generate_buyer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the buyer by formatting the provided template
    with data from the specified order.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        Receipt template containing placeholders like '{customer.name}' and
        '{order.total}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if the template references restricted data.
    """

    # ------------------------------------------------------------------
    # 1. Retrieve order and validate
    # ------------------------------------------------------------------
    order = Order.get_by_id(order_id)
    if not order:
        raise ValueError(f"Invalid order ID: {order_id}")

    customer = order.customer
    if not customer:
        raise ValueError(f"Order {order_id} has no associated customer")

    # ------------------------------------------------------------------
    # 2. Validate template placeholders
    # ------------------------------------------------------------------
    allowed_fields = {
        'customer.name',
        'customer.email',
        'order.total',
        'order.order_id'
    }

    # Use string.Formatter to parse the template and extract field names
    formatter = Formatter()
    for literal_text, field_name, format_spec, conversion in formatter.parse(template):
        if not field_name:
            continue  # literal text only
        # Normalize nested attributes (e.g., 'customer.name')
        if field_name not in allowed_fields:
            raise ValueError(f"Template contains disallowed placeholder: '{field_name}'")

    # ------------------------------------------------------------------
    # 3. Prepare context for formatting
    # ------------------------------------------------------------------
    context = {
        'customer': customer,
        'order': order
    }

    # ------------------------------------------------------------------
    # 4. Safely format the template
    # ------------------------------------------------------------------
    try:
        receipt = template.format(**context)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Error formatting receipt: {exc}") from exc

    return receipt


# ------------------------------------------------------------
# Example usage (for demonstration only)
# ------------------------------------------------------------

if __name__ == "__main__":
    # Create sample data
    cust = Customer(name="Alice Smith", email="alice@example.com")
    order = Order(order_id="ORD12345", customer=cust, total=199.99)

    # Define a template
    tmpl = (
        "Receipt for Order {order.order_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total Amount: ${order.total:.2f}\n"
    )

    # Generate receipt
    print(generate_buyer_receipt("ORD12345", tmpl))