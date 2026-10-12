import re
from dataclasses import dataclass
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mock domain models (would normally be imported from the application)
# ----------------------------------------------------------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str   # Sensitive field – should not be exposed in receipts
    phone: str   # Sensitive field – should not be exposed

@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: list

# ----------------------------------------------------------------------
# In‑memory “database” for demonstration purposes
# ----------------------------------------------------------------------
CUSTOMERS: Dict[str, Customer] = {
    "c001": Customer(id="c001", name="Alice Smith", email="alice@example.com", phone="+123456789"),
    "c002": Customer(id="c002", name="Bob Jones", email="bob@example.com", phone="+987654321"),
}

ORDERS: Dict[str, Order] = {
    "o1001": Order(id="o1001", customer_id="c001", total=149.99, items=["Widget A", "Widget B"]),
    "o1002": Order(id="o1002", customer_id="c002", total=79.50, items=["Gadget X"]),
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_order(order_id: str) -> Order:
    """Retrieve an order by its ID or raise ValueError if not found."""
    try:
        return ORDERS[order_id]
    except KeyError as exc:
        raise ValueError(f"Invalid order ID: {order_id}") from exc

def _get_customer(customer_id: str) -> Customer:
    """Retrieve a customer by its ID or raise ValueError if not found."""
    try:
        return CUSTOMERS[customer_id]
    except KeyError as exc:
        raise ValueError(f"Invalid customer ID: {customer_id}") from exc

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
        A string containing placeholders in the form `{customer.name}` or
        `{order.total}`.

    Returns
    -------
    str
        The receipt string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the order ID is invalid, or if a restricted customer field is requested.
    """
    # Retrieve domain objects
    order = _get_order(order_id)
    customer = _get_customer(order.customer_id)

    # Build a mapping of allowed placeholders to their values
    allowed_fields: Dict[str, Any] = {
        "customer.name": customer.name,
        "order.total": f"{order.total:.2f}",
        # Add other safe fields as needed
    }

    # Identify all placeholders in the template
    placeholder_pattern = r"{([^}]+)}"
    placeholders = re.findall(placeholder_pattern, template)

    # Validate placeholders and construct the replacement mapping
    replacements: Dict[str, str] = {}
    for key in placeholders:
        if key not in allowed_fields:
            # Reject any placeholder that refers to a restricted or unknown field
            raise ValueError(f"Unauthorized or unsupported placeholder: {{{key}}}")
        replacements[key] = allowed_fields[key]

    # Perform the substitution
    def replace(match: re.Match) -> str:
        key = match.group(1)
        return replacements.get(key, match.group(0))

    receipt = re.sub(placeholder_pattern, replace, template)
    return receipt

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Dear {customer.name},\nYour order total is ${order.total}."
#     print(generate_client_receipt("o1001", tmpl))