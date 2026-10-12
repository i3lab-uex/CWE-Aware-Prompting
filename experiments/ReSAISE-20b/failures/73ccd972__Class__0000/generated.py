import re
from typing import Any, Dict

# ----------------------------------------------------------------------
# Mocked domain classes (would normally be imported from the platform)
# ----------------------------------------------------------------------
class Customer:
    """Simple customer model."""
    def __init__(self, name: str, email: str, phone: str,
                 ssn: str = None, password: str = None):
        self.name = name
        self.email = email
        self.phone = phone
        # Sensitive attributes – should never be exposed in a receipt
        self.ssn = ssn
        self.password = password


class Order:
    """Simple order model."""
    def __init__(self, order_id: str, customer: Customer,
                 total: float, items: Dict[str, int]):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items  # e.g., {'widget': 2, 'gadget': 1}


# ----------------------------------------------------------------------
# In‑memory "database" of orders
# ----------------------------------------------------------------------
ORDERS_DB: Dict[str, Order] = {}


def _register_order(order: Order) -> None:
    """Register an order in the mock database."""
    ORDERS_DB[order.order_id] = order


# ----------------------------------------------------------------------
# Receipt creation logic
# ----------------------------------------------------------------------
PLACEHOLDER_PATTERN = re.compile(r"{([^{}]+)}")
RESTRICTED_CUSTOMER_ATTRS = {"ssn", "password"}


def _resolve_placeholder(placeholder: str, order: Order) -> Any:
    """
    Resolve a single placeholder against an Order instance.

    :param placeholder: the placeholder string (e.g., 'customer.name')
    :param order: the Order instance to query
    :return: the resolved value
    :raises ValueError: if accessing a restricted attribute or an invalid path
    """
    parts = placeholder.split(".")
    if not parts:
        raise ValueError(f"Empty placeholder encountered.")

    # Resolve the first part (must be 'order' or 'customer')
    obj: Any
    if parts[0] == "order":
        obj = order
    elif parts[0] == "customer":
        obj = order.customer
    else:
        raise ValueError(f"Unsupported placeholder root '{parts[0]}'.")

    # Traverse remaining attributes
    for attr in parts[1:]:
        if not hasattr(obj, attr):
            raise ValueError(f"Attribute '{attr}' does not exist on {obj}.")
        # Prevent exposing sensitive customer data
        if isinstance(obj, Customer) and attr in RESTRICTED_CUSTOMER_ATTRS:
            raise ValueError(f"Access to restricted customer attribute '{attr}' is denied.")
        obj = getattr(obj, attr)

    return obj


def create_order_receipt(purchase_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given order ID.

    The template may contain placeholders like '{customer.name}' or
    '{order.total}'. Each placeholder is replaced with the corresponding
    value from the Order and Customer objects.

    :param purchase_id: The unique identifier of the order.
    :param receipt_template: A string containing placeholders to replace.
    :return: The fully formatted receipt string.
    :raises ValueError: If the order does not exist or if a placeholder
        attempts to access restricted data.
    """
    # Retrieve the order from the mock database
    order = ORDERS_DB.get(purchase_id)
    if order is None:
        raise ValueError(f"Order with ID '{purchase_id}' does not exist.")

    # Find all placeholders in the template
    placeholders = PLACEHOLDER_PATTERN.findall(receipt_template)

    # Build a mapping of placeholder -> resolved value
    values: Dict[str, Any] = {}
    for ph in placeholders:
        if ph not in values:  # Resolve each placeholder once
            resolved = _resolve_placeholder(ph, order)
            values[ph] = resolved

    # Perform the substitution
    def replacement(match: re.Match) -> str:
        key = match.group(1)
        return str(values.get(key, match.group(0)))

    receipt = PLACEHOLDER_PATTERN.sub(replacement, receipt_template)
    return receipt


# ----------------------------------------------------------------------
# Example usage (for demonstration only – remove in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Create a customer and an order
    cust = Customer(name="Alice Smith", email="alice@example.com",
                    phone="+1234567890", ssn="123-45-6789")
    order = Order(order_id="ORD1001", customer=cust,
                  total=59.99, items={"widget": 2, "gadget": 1})
    _register_order(order)

    # Define a receipt template
    tmpl = (
        "Receipt for Order #{order_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Phone: {customer.phone}\n"
        "Total: ${order.total:.2f}\n"
    )

    # Generate the receipt
    try:
        print(create_order_receipt("ORD1001", tmpl))
    except ValueError as e:
        print(f"Error: {e}")