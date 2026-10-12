import re
from typing import Any, Dict

# ------------------------------------------------------------------
# NOTE: The following minimal stubs are only for demonstration purposes.
# In a real application the `Order`, `Customer` classes and the
# `get_order_by_id` function would be defined elsewhere.
# ------------------------------------------------------------------

class Customer:
    """Simple customer representation."""
    def __init__(self, name: str, email: str, address: str):
        self.name = name
        self.email = email
        self.address = address

class Order:
    """Simple order representation."""
    def __init__(self, id: str, customer: Customer, total: float,
                 date: str, items: list):
        self.id = id
        self.customer = customer
        self.total = total
        self.date = date
        self.items = items

# In-memory "database" of orders for the sake of this example.
_ORDER_DB: Dict[str, Order] = {}

def get_order_by_id(order_id: str) -> Order:
    """Retrieve an order from the mock database."""
    try:
        return _ORDER_DB[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' is invalid.") from exc

# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------

def generate_buyer_receipt(order_id: str, template: str) -> str:
    """
    Generate a formatted receipt for the buyer based on the provided template.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        Receipt pattern containing placeholders such as '{customer.name}' or
        '{order.total}'. Placeholders are replaced with actual data.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid, if restricted data is accessed,
        or if placeholder syntax is malformed.
    """
    # ------------------------------------------------------------------
    # Retrieve the order
    # ------------------------------------------------------------------
    order = get_order_by_id(order_id)

    # ------------------------------------------------------------------
    # Define allowed attributes for security
    # ------------------------------------------------------------------
    ALLOWED_CUSTOMER_ATTRS = {"name", "email", "address"}
    ALLOWED_ORDER_ATTRS = {"total", "date", "items"}

    # ------------------------------------------------------------------
    # Parse placeholders and build a mapping
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"{([^}]+)}")
    mapping: Dict[str, Any] = {}

    for match in placeholder_pattern.finditer(template):
        key_path = match.group(1).strip()
        if "." not in key_path:
            raise ValueError(f"Invalid placeholder '{match.group(0)}': missing '.' separator.")

        obj_name, attr = key_path.split(".", 1)

        if obj_name == "customer":
            if attr not in ALLOWED_CUSTOMER_ATTRS:
                raise ValueError(f"Access to restricted customer attribute '{attr}'.")
            value = getattr(order.customer, attr)
        elif obj_name == "order":
            if attr not in ALLOWED_ORDER_ATTRS:
                raise ValueError(f"Access to restricted order attribute '{attr}'.")
            value = getattr(order, attr)
        else:
            raise ValueError(f"Unknown placeholder object '{obj_name}' in '{match.group(0)}'.")

        mapping[key_path] = value

    # ------------------------------------------------------------------
    # Perform the substitution
    # ------------------------------------------------------------------
    try:
        receipt = template.format(**mapping)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Error formatting receipt: {exc}") from exc

    return receipt


# ------------------------------------------------------------------
# Example usage (for testing purposes only)
# ------------------------------------------------------------------

if __name__ == "__main__":
    # Populate mock database
    cust = Customer(name="Alice Smith", email="alice@example.com",
                    address="123 Maple Street")
    order = Order(id="ORD-001", customer=cust, total=149.99,
                  date="2024-07-23", items=["Laptop", "Mouse"])
    _ORDER_DB[order.id] = order

    tmpl = (
        "Receipt for {customer.name}\n"
        "Email: {customer.email}\n"
        "Address: {customer.address}\n\n"
        "Order ID: {order.id}\n"
        "Date: {order.date}\n"
        "Items: {order.items}\n"
        "Total: ${order.total:.2f}"
    )

    print(generate_buyer_receipt("ORD-001", tmpl))