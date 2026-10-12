import re
from typing import Any

# --------------------------------------------------------------------------- #
# Sample data models (minimal) – in a real system these would be more
# sophisticated and probably come from an ORM or external service.
# --------------------------------------------------------------------------- #

class Customer:
    def __init__(self, customer_id: str, name: str, email: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email  # **Sensitive** – should not be exposed unless authorized


class Order:
    def __init__(self, order_id: str, total: float, currency: str,
                 customer: Customer, items: list):
        self.order_id = order_id
        self.total = total
        self.currency = currency
        self.customer = customer
        self.items = items  # list of dicts e.g. [{'name': 'Widget', 'qty':2, ...}]

# --------------------------------------------------------------------------- #
# Dummy storage / lookup functions – replace with real DB/API calls in prod.
# --------------------------------------------------------------------------- #

def get_order_by_id(order_id: str) -> Order:
    """
    Simulate retrieval of an Order object by ID.
    Raise ValueError if the order does not exist.
    """
    # For demonstration, we create a static order.
    if order_id != "ORD123":
        raise ValueError(f"Order {order_id} not found")
    cust = Customer(customer_id="CUST456", name="Alice Smith",
                    email="alice@example.com")
    items = [
        {"name": "Widget", "qty": 2, "price": 19.99},
        {"name": "Gadget", "qty": 1, "price": 29.99},
    ]
    return Order(order_id=order_id,
                 total=sum(i["price"] * i["qty"] for i in items),
                 currency="USD",
                 customer=cust,
                 items=items)


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _safe_getattr(obj: Any, attr_path: str) -> Any:
    """
    Resolve nested attributes safely.
    Only allows traversal through a whitelist of attribute names to
    prevent accidental exposure of sensitive data.
    """
    # Whitelist of allowed attributes per class type
    whitelist = {
        Order: {"order_id", "total", "currency", "customer", "items"},
        Customer: {"customer_id", "name"},  # email is intentionally excluded
    }

    parts = attr_path.split(".")
    current_obj = obj

    for part in parts:
        if type(current_obj) not in whitelist or part not in whitelist[type(current_obj)]:
            raise ValueError(f"Unauthorized access to attribute '{part}'")
        try:
            current_obj = getattr(current_obj, part)
        except AttributeError as exc:
            raise ValueError(f"Attribute '{part}' not found") from exc

    return current_obj


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def generate_customer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order ID based on the supplied
    template. Placeholders in the form `{order.attribute}` or
    `{customer.attribute}` are replaced with actual data.

    Raises:
        ValueError: If the order cannot be found, a placeholder references
                    an unauthorized attribute, or any other error occurs.
    """
    if not order_id:
        raise ValueError("order_id must be provided")

    # Retrieve the order object
    try:
        order = get_order_by_id(order_id)
    except Exception as exc:
        raise ValueError(f"Failed to retrieve order: {exc}") from exc

    # Prepare a mapping of context objects for placeholder resolution
    context = {
        "order": order,
        "customer": order.customer,
    }

    # Regex to find placeholders like {order.total} or {customer.name}
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")

    def replace_placeholder(match: re.Match) -> str:
        expr = match.group(1).strip()
        if "." not in expr:
            raise ValueError(f"Invalid placeholder format: '{expr}'")
        root, attr_path = expr.split(".", 1)
        if root not in context:
            raise ValueError(f"Unknown placeholder prefix '{root}'")
        try:
            value = _safe_getattr(context[root], attr_path)
            # Convert non-string values to string
            return str(value)
        except ValueError as exc:
            raise ValueError(f"Error resolving placeholder '{expr}': {exc}") from exc

    try:
        receipt = placeholder_pattern.sub(replace_placeholder, template)
    except Exception as exc:
        raise ValueError(f"Failed to generate receipt: {exc}") from exc

    return receipt


# --------------------------------------------------------------------------- #
# Example usage (for testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.order_id}\n"
        "Customer: {customer.name}\n"
        "Total: {order.total} {order.currency}\n"
        "Items:\n{order.items}"
    )
    try:
        print(generate_customer_receipt("ORD123", tmpl))
    except ValueError as e:
        print(f"Error: {e}")