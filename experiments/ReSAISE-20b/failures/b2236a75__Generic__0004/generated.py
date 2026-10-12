import re
from typing import Any

# --- Mock data structures ---------------------------------------------

class Customer:
    def __init__(self, name: str, email: str, address: str):
        self.name = name
        self.email = email
        self.address = address

class Order:
    def __init__(self, order_id: str, total: float, items: list[dict], customer: Customer):
        self.order_id = order_id
        self.total = total
        self.items = items          # e.g. [{'name': 'Widget', 'price': 9.99, 'qty': 2}]
        self.customer = customer

# In a real system these would come from a database
ORDERS_DB = {
    "A001": Order(
        order_id="A001",
        total=59.97,
        items=[{"name": "Widget", "price": 9.99, "qty": 3}],
        customer=Customer(name="Alice Smith", email="alice@example.com",
                          address="123 Maple St, Townsville")
    ),
}

# -----------------------------------------------------------------------

PLACEHOLDER_PATTERN = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

def _resolve_attribute(obj: Any, attr_path: str) -> Any:
    """
    Resolve a dotted attribute path on an object.
    Only public attributes (not starting with '_') are allowed.
    """
    parts = attr_path.split(".")
    current = obj
    for part in parts:
        if part.startswith("_"):
            raise ValueError(f"Access to private attribute '{part}' is forbidden")
        try:
            current = getattr(current, part)
        except AttributeError as exc:
            raise ValueError(f"Attribute '{part}' not found in {current}") from exc
    return current

def generate_customer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string by replacing placeholders in the template with
    values from the order and its associated customer.

    Parameters:
        order_id (str): The ID of the order.
        template (str): The receipt template containing placeholders like
                        '{order.total}' or '{customer.name}'.

    Returns:
        str: The rendered receipt string.

    Raises:
        ValueError: If the order is not found, a placeholder cannot be resolved,
                    or access to sensitive data is attempted.
    """
    # Retrieve order
    order = ORDERS_DB.get(order_id)
    if not order:
        raise ValueError(f"Order with ID '{order_id}' not found")

    # Build a context dictionary for resolution
    context = {
        "order": order,
        "customer": order.customer
    }

    def _replacement(match: re.Match) -> str:
        placeholder = match.group(1)
        if "." not in placeholder:
            raise ValueError(f"Invalid placeholder '{placeholder}'. "
                             "Must be of the form 'order.attr' or 'customer.attr'")
        root, attr_path = placeholder.split(".", 1)
        obj = context.get(root)
        if obj is None:
            raise ValueError(f"Unknown root '{root}' in placeholder")
        value = _resolve_attribute(obj, attr_path)
        return str(value)

    try:
        receipt = PLACEHOLDER_PATTERN.sub(_replacement, template)
    except re.error as exc:
        raise ValueError("Invalid regex pattern in template") from exc

    return receipt


# -----------------------------------------------------------------------
# Example usage
if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.order_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Address: {customer.address}\n"
        "Total: ${order.total:.2f}\n"
    )
    print(generate_customer_receipt("A001", tmpl))