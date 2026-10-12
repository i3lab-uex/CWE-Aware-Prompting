import re
from typing import Dict, Any

# Assume these classes are defined elsewhere in the codebase.
class Order:
    # Example attributes
    id: str
    total: float
    date: str
    items: list  # List of dicts with item details

class Customer:
    # Example attributes
    name: str
    email: str
    address: str

# Mock database access functions (replace with real implementations)
def get_order_by_id(order_id: str) -> Order:
    """Retrieve an Order object by its ID."""
    # In a real implementation this would query a database.
    raise NotImplementedError

def get_customer_by_order(order: Order) -> Customer:
    """Retrieve the Customer associated with a given order."""
    # In a real implementation this would query a database.
    raise NotImplementedError


# Whitelist of allowed placeholders
_ALLOWED_PLACEHOLDERS = {
    "order.total",
    "order.date",
    "order.id",
    "customer.name",
    "customer.email",
    "customer.address",
}

# Mapping of placeholder to a function that extracts the value
def _extract_value(order: Order, customer: Customer, placeholder: str) -> Any:
    if placeholder == "order.total":
        return f"{order.total:.2f}"
    elif placeholder == "order.date":
        return order.date
    elif placeholder == "order.id":
        return order.id
    elif placeholder == "customer.name":
        return customer.name
    elif placeholder == "customer.email":
        return customer.email
    elif placeholder == "customer.address":
        return customer.address
    else:
        # Should never reach here due to whitelist check
        raise ValueError(f"Unsupported placeholder: {placeholder}")


def generate_customer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order ID using the provided template.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A string containing placeholders such as '{order.total}' or '{customer.name}'.

    Returns
    -------
    str
        The rendered receipt with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the order cannot be found, if the template contains unsupported placeholders,
        or if any attempt is made to expose sensitive data.
    """
    # Retrieve order and customer objects
    try:
        order = get_order_by_id(order_id)
    except Exception as exc:
        raise ValueError(f"Order with ID '{order_id}' could not be retrieved.") from exc

    try:
        customer = get_customer_by_order(order)
    except Exception as exc:
        raise ValueError(f"Customer for order '{order_id}' could not be retrieved.") from exc

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^\}]+)\}")
    placeholders_in_template = set(placeholder_pattern.findall(template))

    # Validate that all placeholders are allowed
    for ph in placeholders_in_template:
        if ph not in _ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Unauthorized placeholder detected: '{ph}'")

    # Replace placeholders safely
    def replacement(match):
        ph = match.group(1)
        return str(_extract_value(order, customer, ph))

    try:
        receipt = placeholder_pattern.sub(replacement, template)
    except Exception as exc:
        raise ValueError("An error occurred while rendering the receipt.") from exc

    return receipt