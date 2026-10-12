import re
from typing import Dict

# Assume these classes are provided by the platform's data layer.
# The imports below may need to be adjusted depending on the actual package structure.
try:
    from models import Order, Customer
except ImportError:
    # Minimal stubs for type checking / demonstration purposes.
    class Customer:
        def __init__(self, name: str, email: str):
            self.name = name
            self.email = email

    class Order:
        _store: Dict[str, "Order"] = {}

        def __init__(self, purchase_id: str, total: float, customer: Customer):
            self.purchase_id = purchase_id
            self.total = total
            self.customer = customer
            Order._store[purchase_id] = self

        @classmethod
        def get_by_id(cls, purchase_id: str) -> "Order":
            return cls._store.get(purchase_id)

# -----------------------------------------------------------------------------
# Helper utilities
# -----------------------------------------------------------------------------

ALLOWED_CUSTOMER_FIELDS = {"name", "email"}
ALLOWED_ORDER_FIELDS = {"total", "purchase_id"}

PLACEHOLDER_PATTERN = re.compile(r"\{([^}]+)\}")


def _extract_placeholders(template: str):
    """Yield the placeholder keys found in the template."""
    return PLACEHOLDER_PATTERN.findall(template)


def _build_context(order: Order) -> Dict[str, str]:
    """Construct a mapping from placeholder names to string values."""
    ctx = {}
    # Order-level fields
    for field in ALLOWED_ORDER_FIELDS:
        value = getattr(order, field, None)
        if value is not None:
            ctx[f"order.{field}"] = str(value)

    # Customer-level fields
    customer = order.customer
    for field in ALLOWED_CUSTOMER_FIELDS:
        value = getattr(customer, field, None)
        if value is not None:
            ctx[f"customer.{field}"] = str(value)

    return ctx


def _validate_placeholders(placeholders, context):
    """Ensure all placeholders are present in the allowed context."""
    for key in placeholders:
        if key not in context:
            # Disallow unknown or protected fields
            raise ValueError(f"Invalid or restricted placeholder: '{{{key}}}'")


# -----------------------------------------------------------------------------
# Main function
# -----------------------------------------------------------------------------

def create_order_receipt(purchase_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given purchase ID.

    Parameters
    ----------
    purchase_id : str
        The unique identifier of the order.
    receipt_template : str
        A template string containing placeholders such as '{customer.name}'
        and '{order.total}'.

    Returns
    -------
    str
        The receipt string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the order ID does not exist or a placeholder references disallowed data.
    """
    # Retrieve the order; raise if not found
    order = Order.get_by_id(purchase_id)
    if not order:
        raise ValueError(f"Order with ID '{purchase_id}' does not exist.")

    # Build context mapping
    context = _build_context(order)

    # Find all placeholders in the template
    placeholders = _extract_placeholders(receipt_template)

    # Validate that each placeholder is allowed and present
    _validate_placeholders(placeholders, context)

    # Perform the substitution safely
    def replacement(match):
        key = match.group(1)
        return context[key]

    formatted_receipt = PLACEHOLDER_PATTERN.sub(replacement, receipt_template)
    return formatted_receipt