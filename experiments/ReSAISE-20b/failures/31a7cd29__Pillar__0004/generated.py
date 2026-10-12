import re
from typing import Dict

# ------------------------------------------------------------------
# Mock data structures (would normally be provided by the platform)
# ------------------------------------------------------------------

class Customer:
    """Represents a customer."""
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email
        # phone is considered protected and should not be exposed in receipts
        self._phone = phone

class Order:
    """Represents an order."""
    def __init__(self, identifier: str, customer: Customer,
                 total: float, date: str, items: Dict[str, int]):
        self.identifier = identifier
        self.customer = customer
        self.total = total
        self.date = date
        self.items = items  # e.g., {"widget": 2, "gadget": 1}

# ------------------------------------------------------------------
# Example in‑memory database of orders
# ------------------------------------------------------------------

ORDER_DB: Dict[str, Order] = {}

def add_order(order: Order):
    ORDER_DB[order.identifier] = order

# ------------------------------------------------------------------
# Receipt generation
# ------------------------------------------------------------------

PLACEHOLDER_PATTERN = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

# Allowed attributes for each object
ALLOWED_CUSTOMER_ATTRS = {"name", "email"}
ALLOWED_ORDER_ATTRS   = {"total", "date", "items"}

def _resolve_placeholder(match: re.Match, order: Order) -> str:
    """Resolve a single placeholder from the template."""
    path = match.group(1).split(".")
    if not path:
        raise ValueError("Empty placeholder")

    # Resolve the first object
    obj = order if path[0] == "order" else getattr(order, "customer", None)
    if obj is None:
        raise ValueError(f"Unknown placeholder root: {path[0]}")

    # Determine allowed attributes based on the object type
    if isinstance(obj, Order):
        allowed_attrs = ALLOWED_ORDER_ATTRS
    elif isinstance(obj, Customer):
        allowed_attrs = ALLOWED_CUSTOMER_ATTRS
    else:
        raise ValueError(f"Unsupported object type in placeholder: {type(obj)}")

    # Walk the remaining path
    for attr in path[1:]:
        if attr not in allowed_attrs:
            raise ValueError(f"Access to restricted attribute '{attr}' is forbidden")
        try:
            obj = getattr(obj, attr)
        except AttributeError as exc:
            raise ValueError(f"Attribute '{attr}' not found") from exc

    # Convert non‑string values to string
    return str(obj)

def build_order_receipt(order_identifier: str, template_string: str) -> str:
    """
    Generate a receipt string by substituting placeholders in `template_string`
    with data from the order identified by `order_identifier`.

    Parameters
    ----------
    order_identifier : str
        Unique identifier of the order.
    template_string : str
        Template containing placeholders such as '{customer.name}' or '{order.total}'.

    Returns
    -------
    str
        Formatted receipt string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the order ID does not exist or a placeholder attempts to access
        restricted/protected data.
    """
    # Retrieve the order; raise if missing
    order = ORDER_DB.get(order_identifier)
    if not order:
        raise ValueError(f"Order ID '{order_identifier}' does not exist")

    # Substitute placeholders safely
    try:
        receipt = PLACEHOLDER_PATTERN.sub(
            lambda m: _resolve_placeholder(m, order), template_string
        )
    except ValueError as exc:
        # Re‑raise with context
        raise ValueError(f"Failed to build receipt: {exc}") from exc

    return receipt

# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     cust = Customer(name="Alice", email="alice@example.com", phone="555-1234")
#     ord1 = Order(
#         identifier="ORD001",
#         customer=cust,
#         total=99.95,
#         date="2024-07-23",
#         items={"widget": 2, "gadget": 1}
#     )
#     add_order(ord1)
#
#     tmpl = (
#         "Receipt for Order {order.identifier}\n"
#         "Customer: {customer.name} ({customer.email})\n"
#         "Date: {order.date}\n"
#         "Total: ${order.total}\n"
#     )
#
#     print(build_order_receipt("ORD001", tmpl))