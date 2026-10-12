import re
from typing import Dict, Any

# --------------------------------------------------------------------
# Mocked data models (would normally be imported from the application)
# --------------------------------------------------------------------

class Customer:
    """Represents a customer in the e‑commerce system."""
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email  # Sensitive


class Order:
    """Represents an order in the e‑commerce system."""
    def __init__(self, order_id: str, total: float, customer: Customer):
        self.id = order_id
        self.total = total
        self.customer = customer


# --------------------------------------------------------------------
# In‑memory “database” of orders (for demonstration purposes)
# --------------------------------------------------------------------

_ORDER_DB: Dict[str, Order] = {}

def _load_demo_data() -> None:
    """Populate the in‑memory store with sample data."""
    global _ORDER_DB
    customer = Customer(name="Alice Smith", email="alice@example.com")
    order = Order(order_id="ORD12345", total=149.99, customer=customer)
    _ORDER_DB[order.id] = order

_load_demo_data()


# --------------------------------------------------------------------
# Receipt generation
# --------------------------------------------------------------------

_REPLACE_PATTERN = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

# Fields that are considered sensitive and must not be exposed
_RESTRICTED_FIELDS = {"customer.email"}

def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in _REPLACE_PATTERN.finditer(template)}

def _get_value(order: Order, field_path: str) -> Any:
    """
    Resolve a dotted field path against the order object.
    For example, 'customer.name' will return order.customer.name.
    """
    parts = field_path.split(".")
    obj: Any = order
    for part in parts:
        if not hasattr(obj, part):
            raise ValueError(f"Invalid placeholder '{{{field_path}}}' in template.")
        obj = getattr(obj, part)
    return obj

def generate_client_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt for the given order using the provided template.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A string containing placeholders such as '{customer.name}' or
        '{order.total}'.  Placeholders must correspond to attributes of the
        Order and its Customer.

    Returns
    -------
    str
        The formatted receipt string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the order ID is unknown, or if a placeholder refers to restricted data,
        or if an invalid placeholder is used.
    """
    # 1. Validate the order ID and fetch the order
    order = _ORDER_DB.get(order_id)
    if order is None:
        raise ValueError(f"Order ID '{order_id}' does not exist.")

    # 2. Extract placeholders and check for restricted fields
    placeholders = _extract_placeholders(template)
    if not placeholders:
        return template  # nothing to replace

    for field in placeholders:
        if field in _RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted data '{field}' is not allowed.")

    # 3. Resolve each placeholder value
    values: Dict[str, Any] = {}
    for field in placeholders:
        try:
            value = _get_value(order, field)
        except ValueError as exc:
            raise ValueError(f"Invalid placeholder '{{{field}}}': {exc}") from None
        values[field] = value

    # 4. Perform the substitution safely
    def _replace(match: re.Match) -> str:
        key = match.group(1)
        return str(values[key])

    result = _REPLACE_PATTERN.sub(_replace, template)

    return result

# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------

# if __name__ == "__main__":
#     tmpl = "Hello {customer.name}, your order {order.id} totals ${order.total:.2f}"
#     print(generate_client_receipt("ORD12345", tmpl))