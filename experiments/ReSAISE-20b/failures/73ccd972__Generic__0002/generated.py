import re
from datetime import datetime
from typing import Dict

# --------------------------------------------------------------------------- #
# Mock data structures – in a real system these would come from the database
# --------------------------------------------------------------------------- #

class Customer:
    def __init__(self, name: str, email: str, ssn: str = None):
        self.name = name
        self.email = email
        # Sensitive data that must not be exposed via the receipt template
        self.ssn = ssn

class Order:
    def __init__(self, order_id: str, customer: Customer, total: float, date: datetime):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.date = date

# In‑memory store of orders – replace with real persistence in production
orders: Dict[str, Order] = {}

# --------------------------------------------------------------------------- #
# Helper – mapping of allowed placeholders to their values
# --------------------------------------------------------------------------- #

_ALLOWED_PLACEHOLDERS = {
    "customer.name": lambda o: o.customer.name,
    "customer.email": lambda o: o.customer.email,
    "order.total": lambda o: f"{o.total:.2f}",
    "order.date": lambda o: o.date.strftime("%Y-%m-%d"),
}

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_order_receipt(purchase_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt string for the given order ID.

    Parameters
    ----------
    purchase_id : str
        The unique identifier of the order.
    receipt_template : str
        A template string containing placeholders such as `{customer.name}`.

    Returns
    -------
    str
        The receipt string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the order does not exist or if a restricted field is requested.
    """
    # Retrieve order
    try:
        order = orders[purchase_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{purchase_id}' does not exist.") from exc

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"{([^}]+)}")
    found_placeholders = set(placeholder_pattern.findall(receipt_template))

    # Validate placeholders
    for ph in found_placeholders:
        if ph not in _ALLOWED_PLACEHOLDERS:
            # Disallow access to any other customer attributes
            if ph.startswith("customer.") and ph.split(".", 1)[-1] in ("ssn", "password"):
                raise ValueError(f"Access to restricted field '{ph}' is not allowed.")
            raise ValueError(f"Unknown placeholder '{ph}'. Allowed placeholders: "
                             f"{', '.join(sorted(_ALLOWED_PLACEHOLDERS))}")

    # Build a mapping for format()
    mapping = {ph: _ALLOWED_PLACEHOLDERS[ph](order) for ph in found_placeholders}

    # Replace the template placeholders with keys that format() can use
    # e.g. {customer.name} -> {customer_name}
    def _placeholder_to_key(match: re.Match) -> str:
        ph = match.group(1)
        return f"{{{ph.replace('.', '_')}}}"

    formatted_template = placeholder_pattern.sub(_placeholder_to_key, receipt_template)

    # Convert mapping keys to the new format
    formatted_mapping = {k.replace('.', '_'): v for k, v in mapping.items()}

    # Generate final receipt
    return formatted_template.format(**formatted_mapping)

# --------------------------------------------------------------------------- #
# Example usage (would normally be in tests or separate application code)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Setup sample data
    cust = Customer(name="Alice Smith", email="alice@example.com")
    order = Order(order_id="ORD12345", customer=cust, total=149.99,
                  date=datetime(2024, 7, 22))
    orders[order.order_id] = order

    template = (
        "Receipt for Order #{order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Date: {order.date}\n"
        "Total Amount: ${order.total}"
    )

    # Render receipt
    print(create_order_receipt("ORD12345", template))