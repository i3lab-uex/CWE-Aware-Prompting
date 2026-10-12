import re
from datetime import datetime
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mock models (replace with real imports in production)
# ----------------------------------------------------------------------
class Customer:
    """A minimal customer model."""
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email      # sensitive
        self.phone = phone

class Order:
    """A minimal order model."""
    def __init__(self, transaction_id: str, customer: Customer,
                 total: float, date: datetime):
        self.transaction_id = transaction_id
        self.customer = customer
        self.total = total
        self.date = date

# ----------------------------------------------------------------------
# In‑memory order store (replace with database access in production)
# ----------------------------------------------------------------------
_ORDER_DB: Dict[str, Order] = {}

def register_order(order: Order) -> None:
    """Utility to add an order to the in‑memory store."""
    _ORDER_DB[order.transaction_id] = order

# ----------------------------------------------------------------------
# Allowed placeholders mapping
# ----------------------------------------------------------------------
_ALLOWED_PLACEHOLDERS: Dict[str, Any] = {
    # Customer fields
    'customer.name': lambda o: o.customer.name,
    # Order fields
    'order.total': lambda o: f"${o.total:.2f}",
    'order.date': lambda o: o.date.strftime("%Y-%m-%d"),
}

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_receipt_for_transaction(transaction_id: str, template_format: str) -> str:
    """
    Generate a receipt by substituting placeholders in the given template.

    Args:
        transaction_id: The unique identifier of the order.
        template_format: A string containing placeholders like '{customer.name}'.

    Returns:
        The formatted receipt string with placeholders replaced by actual values.

    Raises:
        ValueError: If the transaction ID does not exist or if a placeholder
                    references restricted data.
    """
    # 1. Retrieve the order
    order = _ORDER_DB.get(transaction_id)
    if not order:
        raise ValueError(f"Order with ID '{transaction_id}' does not exist.")

    # 2. Find all placeholders in the template
    placeholder_pattern = r'\{([^}]+)\}'
    placeholders = re.findall(placeholder_pattern, template_format)

    # 3. Replace each placeholder
    for ph in placeholders:
        if ph not in _ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Unauthorized placeholder '{ph}'.")
        replacement = _ALLOWED_PLACEHOLDERS[ph](order)
        template_format = template_format.replace(f'{{{ph}}}', replacement)

    return template_format

# ----------------------------------------------------------------------
# Example usage (for testing purposes only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Create sample data
    cust = Customer(name="Jane Doe", email="jane@example.com", phone="555-1234")
    order = Order(
        transaction_id="TXN1001",
        customer=cust,
        total=149.99,
        date=datetime(2023, 9, 25)
    )
    register_order(order)

    # Define a template
    tmpl = (
        "Receipt\n"
        "--------\n"
        "Customer: {customer.name}\n"
        "Date: {order.date}\n"
        "Total Amount: {order.total}\n"
    )

    # Generate receipt
    print(create_receipt_for_transaction("TXN1001", tmpl))