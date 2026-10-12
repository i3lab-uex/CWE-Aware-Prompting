import re
from typing import Any

# --- Dummy data structures for illustration ----------------------------
# In a real system these would be provided by the database or ORM.
class Customer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class Order:
    def __init__(self, order_id: str, total: float, customer: Customer):
        self.order_id = order_id
        self.total = total
        self.customer = customer

# Simulated data store
_ORDER_DB = {
    "123": Order("123", 49.99, Customer("Alice Smith", "alice@example.com")),
    "456": Order("456", 79.95, Customer("Bob Jones", "bob@example.com")),
}

def get_order(order_id: str) -> Order:
    """Retrieve an order by its ID. Raise ValueError if not found."""
    try:
        return _ORDER_DB[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' not found") from exc

# -----------------------------------------------------------------------

# List of attribute names that are considered sensitive and must not be accessed.
_SENSITIVE_ATTRS = {"password", "ssn", "credit_card_number", "pin"}

# Regular expression to find placeholders like {order.total} or {customer.name}
_PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

def _safe_get_attr(obj: Any, attr_path: str) -> Any:
    """
    Safely retrieve a nested attribute from an object.
    Raises ValueError if any part of the path is forbidden or missing.
    """
    parts = attr_path.split(".")
    current_obj = obj
    for part in parts:
        # Reject attribute names that look like private or start with an underscore
        if part.startswith("_"):
            raise ValueError(f"Access to private attribute '{part}' is forbidden")
        if part.lower() in _SENSITIVE_ATTRS:
            raise ValueError(f"Access to sensitive attribute '{part}' is forbidden")
        if not hasattr(current_obj, part):
            raise ValueError(f"Attribute '{part}' does not exist on {type(current_obj).__name__}")
        current_obj = getattr(current_obj, part)
    return current_obj

def generate_customer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order ID using the provided template.

    The template may contain placeholders in the form {order.attribute} or
    {customer.attribute}. These are replaced with actual values from the order
    and customer objects. Access to private or sensitive attributes is blocked.

    Parameters:
        order_id (str): The ID of the order to generate a receipt for.
        template (str): A string containing placeholders.

    Returns:
        str: The formatted receipt string.

    Raises:
        ValueError: If the order cannot be found, a placeholder refers to
                    an invalid or sensitive attribute, or any other error occurs.
    """
    # Retrieve the order; this may raise ValueError if not found
    order = get_order(order_id)

    # Prepare a dictionary of objects that can be referenced in the template
    context = {"order": order, "customer": order.customer}

    # Function to replace each placeholder
    def _replace(match: re.Match) -> str:
        key = match.group(1)
        if "." not in key:
            # Allow direct reference to order or customer
            if key not in context:
                raise ValueError(f"Unknown placeholder '{key}'")
            value = context[key]
        else:
            # Resolve nested attribute chain
            root, attr_chain = key.split(".", 1)
            if root not in context:
                raise ValueError(f"Unknown root object '{root}'")
            value = _safe_get_attr(context[root], attr_chain)
        # Convert non-string values to string
        return str(value)

    try:
        receipt = _PLACEHOLDER_RE.sub(_replace, template)
    except Exception as exc:
        raise ValueError(f"Failed to generate receipt: {exc}") from exc

    return receipt

# -----------------------------------------------------------------------
# Example usage (uncomment to test):
# if __name__ == "__main__":
#     tmpl = "Order {order.order_id} for {customer.name}\nTotal: ${order.total}"
#     print(generate_customer_receipt("123", tmpl))