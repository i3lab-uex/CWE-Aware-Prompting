import re
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mock data structures (in a real system these would be imported)
# ----------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str, address: str, _credit_card: str):
        self.name = name
        self.email = email
        self.address = address
        # underscore indicates protected field
        self._credit_card = _credit_card

class Order:
    def __init__(self, order_id: str, customer: Customer,
                 items: Dict[str, float], total: float):
        self.order_id = order_id
        self.customer = customer
        self.items = items          # e.g., {"widget": 2, "gadget": 1}
        self.total = total

# ----------------------------------------------------------------------
# In‑memory order store (replace with real DB in production)
# ----------------------------------------------------------------------
_orders: Dict[str, Order] = {}

def add_order(order: Order) -> None:
    """Utility to populate the order store."""
    _orders[order.order_id] = order

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
PLACEHOLDER_RE = re.compile(r"{([^{}]+)}")

def _resolve_placeholder(key: str, order: Order) -> Any:
    """
    Resolve a single placeholder key against an Order instance.
    Raises ValueError if the key refers to protected data or does not exist.
    """
    # Support nested attributes e.g. customer.name
    parts = key.split(".")
    obj: Any = order
    for part in parts:
        if not hasattr(obj, part):
            raise ValueError(f"Invalid placeholder '{key}': attribute '{part}' not found.")
        # Prevent access to protected attributes
        if part.startswith("_"):
            raise ValueError(f"Attempted to access protected attribute '{part}'.")
        obj = getattr(obj, part)
    return obj

def _render_template(template: str, order: Order) -> str:
    """
    Replace all placeholders in the template with actual values from the order.
    """
    def repl(match: re.Match) -> str:
        key = match.group(1).strip()
        value = _resolve_placeholder(key, order)
        return str(value)

    return PLACEHOLDER_RE.sub(repl, template)

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def compose_invoice_template(invoice_id: str, receipt_format: str) -> str:
    """
    Generate a formatted receipt string for the given order ID.

    Parameters
    ----------
    invoice_id : str
        Identifier of the order.
    receipt_format : str
        Template string containing placeholders such as '{customer.name}'.

    Returns
    -------
    str
        The rendered receipt string.

    Raises
    ------
    ValueError
        If the invoice_id is unknown or if a placeholder refers to protected data.
    """
    # Retrieve order
    order = _orders.get(invoice_id)
    if not order:
        raise ValueError(f"Invalid invoice ID: {invoice_id}")

    # Render the template
    return _render_template(receipt_format, order)

# ----------------------------------------------------------------------
# Example usage (comment out in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Create a customer and an order
    cust = Customer("Alice Smith", "alice@example.com",
                    "123 Maple Street, Springfield", _credit_card="4111-1111-1111-1111")
    order = Order("INV12345", cust, {"widget": 3, "gadget": 2}, total=149.99)

    # Add to store
    add_order(order)

    # Define a receipt template
    tmpl = (
        "Invoice #{invoice_id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Address: {customer.address}\n"
        "Items:\n"
        "{items}\n"
        "Total: ${order.total}"
    )

    # Replace items manually for demonstration
    item_lines = "\n".join([f"  {k}: {v}" for k, v in order.items.items()])
    receipt = compose_invoice_template("INV12345", tmpl.replace("{items}", item_lines))
    print(receipt)