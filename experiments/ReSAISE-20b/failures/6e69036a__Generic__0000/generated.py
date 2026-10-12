import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Mocked data layer – in a real application these would be fetched
# from a database or external service.
# ----------------------------------------------------------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str
    # Some attributes are considered restricted and must not be exposed.
    _ssn: str = field(repr=False, default="")  # Social Security Number (restricted)

@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: list[str]

# Sample data
CUSTOMERS: Dict[str, Customer] = {
    "cust1": Customer(id="cust1", name="Alice Smith", email="alice@example.com", _ssn="123-45-6789"),
    "cust2": Customer(id="cust2", name="Bob Jones", email="bob@example.com"),
}

ORDERS: Dict[str, Order] = {
    "ord001": Order(id="ord001", customer_id="cust1", total=59.99, items=["Widget A", "Widget B"]),
    "ord002": Order(id="ord002", customer_id="cust2", total=120.00, items=["Gadget X"]),
}

# ----------------------------------------------------------------------
# Utility helpers
# ----------------------------------------------------------------------
_REPLACE_PATTERN = re.compile(r"\{([^{}]+)\}")

def _get_attribute(obj, attr_path: str):
    """
    Safely retrieve nested attributes from an object.
    Raises AttributeError if any attribute in the path is missing or restricted.
    """
    attrs = attr_path.split(".")
    current_obj = obj
    for attr in attrs:
        # Prevent access to private attributes (starting with underscore)
        if attr.startswith("_"):
            raise AttributeError(f"Access to restricted attribute '{attr}' is denied.")
        if not hasattr(current_obj, attr):
            raise AttributeError(f"Attribute '{attr}' does not exist on {type(current_obj).__name__}.")
        current_obj = getattr(current_obj, attr)
    return current_obj

def _build_context(order: Order, customer: Customer) -> Dict[str, str]:
    """
    Build a flat dictionary mapping placeholder names to string values.
    """
    context = {
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "order.items": ", ".join(order.items),
        "customer.id": customer.id,
        "customer.name": customer.name,
        "customer.email": customer.email,
    }
    return context

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_client_receipt(order_id: str, template: str) -> str:
    """
    Generate a formatted receipt for the given order using the provided template.
    
    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A string containing placeholders in the form `{entity.attribute}`.
    
    Returns
    -------
    str
        The receipt string with placeholders replaced by actual data.
    
    Raises
    ------
    ValueError
        If the order ID is invalid, or if restricted data is accessed.
    """
    # Validate and fetch the order
    order = ORDERS.get(order_id)
    if not order:
        raise ValueError(f"Order ID '{order_id}' is invalid or does not exist.")
    
    # Fetch the associated customer
    customer = CUSTOMERS.get(order.customer_id)
    if not customer:
        raise ValueError(f"Customer for order '{order_id}' not found.")
    
    # Build context dictionary
    context = _build_context(order, customer)
    
    # Find all placeholders in the template
    placeholders = set(_REPLACE_PATTERN.findall(template))
    
    # Resolve each placeholder
    resolved_values = {}
    for key in placeholders:
        try:
            value = _get_attribute(customer if key.startswith("customer") else order, key)
        except AttributeError as exc:
            raise ValueError(f"Invalid placeholder or restricted data access: {key}") from exc
        resolved_values[key] = str(value)
    
    # Perform safe replacement
    def _replace(match):
        placeholder = match.group(1)
        return resolved_values.get(placeholder, f"{{{placeholder}}}")
    
    receipt = _REPLACE_PATTERN.sub(_replace, template)
    return receipt

# ----------------------------------------------------------------------
# Example usage (commented out – remove comments to run)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total}\n"
        "Items: {order.items}"
    )
    print(generate_client_receipt("ord001", tmpl))