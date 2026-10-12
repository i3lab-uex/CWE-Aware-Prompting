import re
from typing import Any

# ----------------------------------------------------------------------
# Minimal stubs for Order and Customer used only to demonstrate the
# implementation.  In a real system these would be imported from the
# platform's domain modules.
# ----------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str):
        self.name = name          # public
        self.email = email        # public
        self._ssn = "123-45-6789"  # protected

class Order:
    def __init__(self, order_id: str, customer: Customer,
                 total: float, items: list[str]):
        self.order_id = order_id  # public
        self.customer = customer  # public
        self.total = total        # public
        self.items = items        # public

# ----------------------------------------------------------------------
# In-memory store to simulate database access.
# ----------------------------------------------------------------------
_ORDER_DB = {
    "A001": Order("A001", Customer("Alice Smith", "alice@example.com"),
                  250.00, ["Widget A", "Widget B"]),
    "B002": Order("B002", Customer("Bob Jones", "bob@example.com"),
                  120.50, ["Widget C"]),
}

def _get_order_by_id(order_id: str) -> Order:
    """Retrieve an Order instance by ID or raise ValueError."""
    order = _ORDER_DB.get(order_id)
    if not order:
        raise ValueError(f"Invalid order ID: {order_id!r}")
    return order

# ----------------------------------------------------------------------
# Utility to safely resolve attribute paths.
# ----------------------------------------------------------------------
def _resolve_path(obj: Any, path: str) -> Any:
    """
    Resolve a dotted attribute path on *obj*.
    Raises ValueError if the path attempts to access a protected
    attribute (starting with an underscore).
    """
    parts = path.split(".")
    current: Any = obj
    for part in parts:
        if part.startswith("_"):
            raise ValueError(f"Attempt to access protected attribute: {path!r}")
        if not hasattr(current, part):
            raise ValueError(f"Attribute '{part}' not found in {current!r}")
        current = getattr(current, part)
    return current

# ----------------------------------------------------------------------
# Main function to create a purchase receipt.
# ----------------------------------------------------------------------
def create_purchase_receipt(order_id: str, receipt_template: str) -> str:
    """
    Generate a formatted purchase receipt for the given *order_id* using
    *receipt_template*.  The template may contain placeholders like
    `{customer.name}` or `{order.total}`.  Only public attributes are
    allowed; any attempt to reference a protected attribute (starting with
    an underscore) will raise ValueError.

    Parameters
    ----------
    order_id : str
        Identifier of the order to retrieve.
    receipt_template : str
        Template string containing placeholders.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If *order_id* is invalid or if a placeholder references a protected
        attribute.
    """
    # Retrieve the order; this will raise ValueError for invalid IDs.
    order = _get_order_by_id(order_id)

    # Prepare a mapping of the two top-level objects that can be referenced.
    context = {
        "order": order,
        "customer": order.customer,
    }

    # Find all placeholders in the template.
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    matches = placeholder_pattern.findall(receipt_template)

    # Resolve each placeholder and build a replacement dictionary.
    replacements = {}
    for key in matches:
        # The key may be nested (e.g., "customer.name").
        if "." not in key:
            raise ValueError(f"Invalid placeholder format: {{{key}}}")
        top, subpath = key.split(".", 1)
        if top not in context:
            raise ValueError(f"Unknown placeholder prefix: {top!r}")
        value = _resolve_path(context[top], subpath)
        replacements[key] = str(value)

    # Perform the replacement safely.
    def _replace(match: re.Match) -> str:
        inner = match.group(1)
        return replacements.get(inner, match.group(0))

    receipt = placeholder_pattern.sub(_replace, receipt_template)
    return receipt

# ----------------------------------------------------------------------
# Example usage (uncomment to test).
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = (
#         "Receipt for Order {order.order_id}\n"
#         "Customer: {customer.name}\n"
#         "Total: ${order.total:.2f}\n"
#         "Items:\n{order.items}"
#     )
#     print(create_purchase_receipt("A001", template))