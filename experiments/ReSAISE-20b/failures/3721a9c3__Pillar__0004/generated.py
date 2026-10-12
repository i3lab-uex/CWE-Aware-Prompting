import re
from typing import Dict, Any

# Assume these classes are defined elsewhere in the application.
# They are imported here for type hints and to illustrate usage.
from ecommerce.models import Order, Customer


class RestrictedDataAccessError(ValueError):
    """Raised when attempting to access restricted customer data."""


def _build_context(order: Order) -> Dict[str, Any]:
    """
    Construct a flat dictionary that maps placeholder names to values.
    Nested attributes are represented with dot notation (e.g., 'customer.name').
    """
    customer = order.customer
    context: Dict[str, Any] = {
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "order.date": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "customer.id": customer.id,
        "customer.name": f"{customer.first_name} {customer.last_name}",
        "customer.email": customer.email,
    }
    return context


def _validate_template(template: str, context_keys: set[str]) -> None:
    """
    Ensure that every placeholder in the template is present in the context.
    Raises ValueError if an unknown placeholder is found.
    """
    placeholders = set(re.findall(r"\{([^{}]+)\}", template))
    missing = placeholders - context_keys
    if missing:
        raise ValueError(f"Unknown placeholder(s) in template: {', '.join(sorted(missing))}")


def generate_buyer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt for the buyer by filling in placeholders in ``template`` with
    data from the order identified by ``order_id``.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        Receipt template containing placeholders such as '{customer.name}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid, if restricted customer data would be exposed,
        or if the template contains unknown placeholders.
    """
    # Retrieve order; raise ValueError if not found
    try:
        order = Order.get_by_id(order_id)
    except Exception as exc:  # Generic exception for illustration
        raise ValueError(f"Order with ID '{order_id}' not found") from exc

    # Enforce security: disallow access to restricted data
    if getattr(order.customer, "restricted", False):
        raise RestrictedDataAccessError("Attempted to access restricted customer data")

    # Build context mapping for template formatting
    context = _build_context(order)

    # Validate that the template uses only known placeholders
    _validate_template(template, set(context.keys()))

    # Perform safe formatting
    try:
        receipt = template.format(**context)
    except KeyError as exc:  # Should not happen due to validation
        raise ValueError(f"Missing data for placeholder {exc}") from exc

    return receipt