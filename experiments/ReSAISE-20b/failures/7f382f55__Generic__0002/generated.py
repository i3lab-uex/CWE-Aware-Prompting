import re
from typing import Dict, Any

# ----------------------------------------------------------------------
# Minimal domain model (would normally be provided by the platform)
# ----------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str, address: str):
        self.name = name
        self.email = email
        self.address = address
        # Protected attribute (should not be exposed via the template)
        self._credit_score = 750

class Order:
    def __init__(self, order_id: str, customer: Customer, total: float, items: list):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items

# ----------------------------------------------------------------------
# In‑memory repository of orders (mocked for this example)
# ----------------------------------------------------------------------
ORDER_REPOSITORY: Dict[str, Order] = {}

def _add_order(order: Order) -> None:
    """Helper to populate the repository."""
    ORDER_REPOSITORY[order.order_id] = order

# ----------------------------------------------------------------------
# Utility for safe attribute resolution
# ----------------------------------------------------------------------
def _resolve_placeholder(obj: Any, attr_path: str) -> Any:
    """
    Resolve a dotted attribute path on an object.
    Raises ValueError if the attribute is protected or does not exist.
    """
    parts = attr_path.split('.')
    current = obj
    for part in parts:
        if part.startswith('_'):
            raise ValueError(f"Access to protected attribute '{part}' is forbidden.")
        if not hasattr(current, part):
            raise ValueError(f"Attribute '{part}' not found in object of type {type(current).__name__}.")
        current = getattr(current, part)
    return current

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def compose_invoice_template(invoice_id: str, receipt_format: str) -> str:
    """
    Generate a receipt string for the given invoice ID using the supplied template.

    Parameters
    ----------
    invoice_id : str
        Identifier of the order to retrieve.
    receipt_format : str
        Template string containing placeholders such as '{customer.name}' or
        '{order.total}'. Placeholders are resolved against the Order instance.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the invoice ID is not found, or if a placeholder attempts to access
        a protected attribute of an object.
    """
    # Retrieve the order; raise if not found
    order = ORDER_REPOSITORY.get(invoice_id)
    if order is None:
        raise ValueError(f"Order with ID '{invoice_id}' does not exist.")

    # Regex to find all placeholders like {customer.name}
    placeholder_pattern = re.compile(r'\{([^\{\}]+)\}')

    def replace_placeholder(match: re.Match) -> str:
        placeholder = match.group(1).strip()
        try:
            value = _resolve_placeholder(order, placeholder)
        except ValueError as exc:
            raise ValueError(f"Invalid placeholder '{placeholder}': {exc}") from None
        # Convert non‑string values to string for formatting
        return str(value)

    # Perform the substitution safely
    receipt = placeholder_pattern.sub(replace_placeholder, receipt_format)
    return receipt

# ----------------------------------------------------------------------
# Example usage (for illustration only; remove in production code)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Create sample data
    cust = Customer(name="Jane Doe", email="jane@example.com", address="123 Elm St")
    order = Order(order_id="INV-001", customer=cust, total=199.99,
                  items=[{"sku": "ABC123", "qty": 2, "price": 49.99},
                         {"sku": "XYZ789", "qty": 1, "price": 99.99}])
    _add_order(order)

    template = (
        "Invoice #{order_id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Address: {customer.address}\n"
        "Total: ${order.total:.2f}\n"
    )

    try:
        print(compose_invoice_template("INV-001", template))
    except ValueError as e:
        print(f"Error generating receipt: {e}")