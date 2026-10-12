import re
from typing import Dict

# Assuming these classes are defined elsewhere in the application.
# They should expose public attributes for use in the receipt template.
class Order:
    # Example minimal implementation
    def __init__(self, order_id: str, customer, total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total

class Customer:
    # Example minimal implementation
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

# Dummy in‑memory storage for the example. In real code this would query a database.
ORDERS_DB: Dict[str, Order] = {}

def _get_order(order_id: str) -> Order:
    """Retrieve an order by ID, raising ValueError if not found."""
    try:
        return ORDERS_DB[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' does not exist.") from exc

def _safe_attr(obj, attr: str):
    """Return attribute value if it exists and is not protected."""
    if attr.startswith("_"):
        raise ValueError(f"Access to protected attribute '{attr}' is forbidden.")
    if not hasattr(obj, attr):
        raise ValueError(f"Attribute '{attr}' not found on object of type {type(obj).__name__}.")
    return getattr(obj, attr)

def _build_context(order: Order) -> Dict[str, str]:
    """Build a flat context dictionary for string formatting."""
    context = {}
    # Order attributes
    for key in dir(order):
        if key.startswith("_"):
            continue
        try:
            val = _safe_attr(order, key)
            context[key] = str(val)
        except ValueError:
            continue

    # Customer attributes
    customer = order.customer
    for key in dir(customer):
        if key.startswith("_"):
            continue
        try:
            val = _safe_attr(customer, key)
            context[f"customer.{key}"] = str(val)
        except ValueError:
            continue

    return context

_placeholder_pattern = re.compile(r"{([^{}]+)}")

def compose_invoice_template(invoice_id: str, receipt_format: str) -> str:
    """
    Generate a receipt string for the given invoice ID using the provided template.

    Parameters
    ----------
    invoice_id : str
        Identifier of the order.
    receipt_format : str
        Template string containing placeholders like '{customer.name}' or '{order.total}'.

    Returns
    -------
    str
        The formatted receipt string with placeholders replaced by actual values.

    Raises
    ------
    ValueError
        If the invoice ID is invalid, or if a placeholder refers to a protected attribute.
    """
    order = _get_order(invoice_id)
    context = _build_context(order)

    def replace(match: re.Match) -> str:
        key = match.group(1)
        if key not in context:
            raise ValueError(f"Placeholder '{key}' cannot be resolved.")
        return context[key]

    try:
        receipt = _placeholder_pattern.sub(replace, receipt_format)
    except ValueError as exc:
        raise

    return receipt