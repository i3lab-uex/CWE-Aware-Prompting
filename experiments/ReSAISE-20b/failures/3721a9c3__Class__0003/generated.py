import re
from typing import Dict, Any

# --- Mocked data structures for demonstration purposes ---------------------

class Customer:
    """
    Represents a customer.  The `is_authorized` flag indicates whether
    the caller is allowed to view sensitive customer data.
    """
    def __init__(self, name: str, email: str, ssn: str, is_authorized: bool):
        self.name = name
        self.email = email          # considered sensitive
        self.ssn = ssn              # highly sensitive
        self.is_authorized = is_authorized

class Order:
    """
    Represents an order.
    """
    def __init__(self, order_id: str, total: float, date: str,
                 customer: Customer):
        self.order_id = order_id
        self.total = total
        self.date = date
        self.customer = customer

# -------------------------------------------------------------------------

# A very small in‑memory "database" for demo purposes.
ORDER_DB: Dict[str, Order] = {}

def get_order(order_id: str) -> Order | None:
    """Retrieve an order by ID, or None if it does not exist."""
    return ORDER_DB.get(order_id)

# -------------------------------------------------------------------------

def _sanitize_placeholder(placeholder: str) -> bool:
    """
    Validate that the placeholder is allowed to be expanded.
    Allowed placeholders are limited to non‑sensitive fields of
    Order and Customer.  Any attempt to access sensitive data
    (e.g., email, ssn) will be rejected.
    """
    allowed = {
        'order.order_id',
        'order.total',
        'order.date',
        'customer.name',  # name is considered non‑sensitive
    }
    return placeholder in allowed

def generate_buyer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt for the buyer by filling in placeholders
    from the provided template.

    Parameters:
        order_id (str): The unique identifier of the order.
        template (str): A format string containing placeholders such as
                        '{customer.name}', '{order.total}'.

    Returns:
        str: The formatted receipt string.

    Raises:
        ValueError: If the order ID is invalid, if the customer data
                    is restricted, or if the template contains an
                    disallowed placeholder.
    """
    # 1. Retrieve the order; raise if not found
    order = get_order(order_id)
    if order is None:
        raise ValueError(f"Order ID '{order_id}' does not exist.")

    # 2. Ensure the customer is authorized to view sensitive data
    if not order.customer.is_authorized:
        raise ValueError("Unauthorized access to customer data.")

    # 3. Validate placeholders in the template
    placeholder_pattern = r'\{([^\}]+)\}'
    for match in re.finditer(placeholder_pattern, template):
        placeholder = match.group(1).strip()
        if not _sanitize_placeholder(placeholder):
            raise ValueError(f"Disallowed placeholder detected: '{placeholder}'")

    # 4. Build a safe mapping for str.format
    data_map: Dict[str, Any] = {
        'order.order_id': order.order_id,
        'order.total': f"${order.total:,.2f}",
        'order.date': order.date,
        'customer.name': order.customer.name,
    }

    # 5. Perform formatting
    try:
        receipt = template.format(**data_map)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from None

    return receipt

# -------------------------------------------------------------------------
# Example usage (would normally be in a separate test module)

if __name__ == "__main__":
    # Populate mock database
    cust = Customer(name="Alice Smith",
                    email="alice@example.com",
                    ssn="123-45-6789",
                    is_authorized=True)
    ORDER_DB["ORD123"] = Order(order_id="ORD123",
                               total=149.99,
                               date="2026-07-23",
                               customer=cust)

    tmpl = ("Receipt\n"
            "Order ID: {order.order_id}\n"
            "Date: {order.date}\n"
            "Customer: {customer.name}\n"
            "Total: {order.total}")

    print(generate_buyer_receipt("ORD123", tmpl))