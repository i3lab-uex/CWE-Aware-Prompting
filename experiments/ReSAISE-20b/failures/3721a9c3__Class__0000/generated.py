import re
from typing import Any, Dict

# Assume these classes are defined elsewhere in the application.
# For demonstration purposes, simple stubs are provided below.
class Customer:
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email          # Sensitive
        self.phone = phone

class Order:
    def __init__(self, order_id: str, customer: Customer, total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total

# Dummy in‑memory datastore for illustration. In a real system this would be
# replaced by a database or an external service.
ORDERS_DB: Dict[str, Order] = {}

def _sanitize_placeholder(name: str) -> str:
    """
    Validate placeholder names to avoid leaking sensitive data.
    Disallow any attribute that starts with an underscore or is listed
    in the restricted set. Raise ValueError on violation.
    """
    restricted = {"email", "ssn", "credit_card_number"}
    if name.startswith("_"):
        raise ValueError(f"Access to restricted attribute '{name}' is not allowed.")
    if name in restricted:
        raise ValueError(f"Access to restricted attribute '{name}' is not allowed.")
    return name

def generate_buyer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt for the buyer by replacing placeholders in `template`
    with data from the order and its customer.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        Receipt template containing placeholders like '{customer.name}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is not found or if a restricted attribute is accessed.
    """
    # Retrieve the order from the datastore
    order = ORDERS_DB.get(order_id)
    if not order:
        raise ValueError(f"Order ID '{order_id}' is invalid or does not exist.")

    # Build a dictionary of allowed attributes
    data: Dict[str, Any] = {
        "order_id": order.order_id,
        "order_total": f"{order.total:.2f}",
    }

    # Customer attributes are prefixed with 'customer.'
    for attr in ("name", "phone"):
        data[f"customer.{attr}"] = getattr(order.customer, attr)

    # Regular expression to find placeholders like {customer.name}
    placeholder_pattern = re.compile(r"\{([^}]+)\}")

    def _replacement(match: re.Match) -> str:
        key = match.group(1)
        # Validate the placeholder
        _sanitize_placeholder(key.split('.')[0] if '.' in key else key)
        # Retrieve value
        if key not in data:
            raise ValueError(f"Unknown placeholder '{key}'.")
        return str(data[key])

    # Perform the substitution safely
    receipt = placeholder_pattern.sub(_replacement, template)
    return receipt

# --------------------------------------------------------------------
# Example usage (would normally be in a separate test module)

if __name__ == "__main__":
    # Setup demo data
    cust = Customer(name="Alice Smith", email="alice@example.com", phone="+123456789")
    order = Order(order_id="ORD001", customer=cust, total=199.99)
    ORDERS_DB[order.order_id] = order

    tmpl = (
        "Receipt for Order {order_id}\n"
        "Customer: {customer.name}\n"
        "Phone: {customer.phone}\n"
        "Total Amount: ${order_total}"
    )

    print(generate_buyer_receipt("ORD001", tmpl))