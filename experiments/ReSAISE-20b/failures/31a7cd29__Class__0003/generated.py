import re
from typing import Any, Dict

# ------------------------------------------------------------------
# The following classes are assumed to exist in the application
# environment.  They are included here only as minimal stubs so that
# this module can be executed in isolation for testing purposes.
# In a real deployment they would be imported from the platform's
# domain model.

class Customer:
    def __init__(self, name: str, address: str, email: str, phone: str):
        self.name = name
        self.address = address
        # The following fields are considered *restricted* and must not
        # be exposed in a receipt unless explicitly allowed.
        self.email = email
        self.phone = phone


class Order:
    def __init__(self, order_id: str, customer: Customer,
                 total: float, items: list[Dict[str, Any]]):
        self.id = order_id
        self.customer = customer
        self.total = total
        self.items = items


# ------------------------------------------------------------------
# In a real system the following function would query the database
# or cache to retrieve an Order instance.  For this example it simply
# looks up a predefined dictionary.

ORDERS_DB: Dict[str, Order] = {}


def get_order_by_id(order_id: str) -> Order | None:
    """Retrieve an order by its identifier."""
    return ORDERS_DB.get(order_id)


# ------------------------------------------------------------------
# Core functionality

# Allowed placeholders for the customer object.
ALLOWED_CUSTOMER_FIELDS = {"name", "address"}
# Allowed placeholders for the order object (excluding nested objects).
ALLOWED_ORDER_FIELDS = {"total", "id"}

# Regular expression to find placeholders in the template.
PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")


def _resolve_placeholder(path: str, order: Order) -> Any:
    """
    Resolve a dotted path (e.g. 'customer.name') against an Order instance.
    Raises ValueError if the path references a restricted attribute.
    """
    parts = path.split(".")
    if not parts:
        raise ValueError(f"Empty placeholder in template")

    # Resolve the root object.
    if parts[0] == "customer":
        obj = order.customer
        allowed_fields = ALLOWED_CUSTOMER_FIELDS
    elif parts[0] == "order":
        obj = order
        allowed_fields = ALLOWED_ORDER_FIELDS
    else:
        raise ValueError(f"Unknown root object '{parts[0]}' in placeholder")

    # Resolve nested attributes one by one.
    for attr in parts[1:]:
        if not hasattr(obj, attr):
            raise ValueError(f"Attribute '{attr}' does not exist on {obj}")
        # Check for restricted fields.
        if attr in {"email", "phone"}:
            raise ValueError(f"Access to restricted field '{attr}' is forbidden")
        # If we are still nested, continue.
        obj = getattr(obj, attr)
    return obj


def build_order_receipt(order_identifier: str, template_string: str) -> str:
    """
    Generate a receipt by substituting placeholders in the provided
    template with data from the specified order.

    Parameters:
        order_identifier (str): Unique identifier of the order.
        template_string   (str): Receipt template containing placeholders.

    Returns:
        str: The formatted receipt with all allowed placeholders replaced.

    Raises:
        ValueError: If the order does not exist, or if a placeholder
                    references disallowed data.
    """
    # Retrieve the order; raise error if missing.
    order = get_order_by_id(order_identifier)
    if not order:
        raise ValueError(f"Order '{order_identifier}' does not exist")

    # Find all placeholders in the template.
    placeholders = PLACEHOLDER_RE.findall(template_string)

    # Resolve each placeholder and build a mapping.
    resolved: Dict[str, str] = {}
    for ph in placeholders:
        if ph in resolved:
            continue  # already processed
        try:
            value = _resolve_placeholder(ph, order)
        except ValueError as exc:
            raise ValueError(f"Invalid placeholder '{{{ph}}}': {exc}") from None
        # Convert the value to string for formatting.
        resolved[ph] = str(value)

    # Perform substitution.  We use a custom formatter to avoid
    # accidental access to non‑existent keys.
    def replace(match: re.Match) -> str:
        key = match.group(1)
        return resolved.get(key, match.group(0))

    receipt = PLACEHOLDER_RE.sub(replace, template_string)
    return receipt


# ------------------------------------------------------------------
# Example usage (for demonstration only; remove or comment out in production)

if __name__ == "__main__":
    # Setup a sample order.
    cust = Customer(name="Alice Smith",
                    address="123 Maple St, Springfield",
                    email="alice@example.com",
                    phone="555-0100")
    order = Order(order_id="ORD001", customer=cust,
                  total=199.99, items=[{"name": "Widget", "qty": 2}])
    ORDERS_DB[order.id] = order

    template = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name}\n"
        "Address: {customer.address}\n"
        "Total: ${order.total:.2f}\n"
    )

    try:
        print(build_order_receipt("ORD001", template))
    except ValueError as e:
        print(f"Error: {e}")