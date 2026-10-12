import re
from typing import Dict

# Assume these classes are defined elsewhere in the codebase.
# They must provide a `get_by_id` class method that returns an instance.
class Order:
    # Example attributes – real implementation will have more
    order_id: str
    total: float
    items: list  # list of dicts with 'name', 'quantity', 'price'
    customer_id: str

    @classmethod
    def get_by_id(cls, order_id: str) -> "Order":
        """Retrieve an Order instance by its ID.
        Replace with actual data access logic (e.g., database query)."""
        raise NotImplementedError


class Customer:
    # Example attributes – real implementation will have more
    customer_id: str
    name: str
    email: str

    @classmethod
    def get_by_id(cls, customer_id: str) -> "Customer":
        """Retrieve a Customer instance by its ID."""
        raise NotImplementedError


# Whitelist of allowed placeholder keys.
_ALLOWED_KEYS = {
    "order.total",
    "order.items",  # Serialized as JSON string
    "customer.name",
    "customer.email",
}


def _safe_str(value) -> str:
    """Return a string representation that cannot contain control characters."""
    if isinstance(value, (list, dict)):
        import json

        return json.dumps(value)
    return str(value)


def generate_customer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order using the provided template.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A receipt template containing placeholders such as `{order.total}` or `{customer.name}`.

    Returns
    -------
    str
        The rendered receipt string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the order cannot be found, if the template contains disallowed placeholders,
        or if any other error occurs during rendering.
    """
    try:
        # Retrieve order and customer objects
        order = Order.get_by_id(order_id)
        if not isinstance(order, Order):
            raise ValueError(f"Order with id {order_id} not found")

        customer = Customer.get_by_id(order.customer_id)
        if not isinstance(customer, Customer):
            raise ValueError(f"Customer with id {order.customer_id} not found")

        # Build a mapping of allowed placeholders to values
        context: Dict[str, str] = {
            "order.total": _safe_str(order.total),
            "order.items": _safe_str(order.items),
            "customer.name": _safe_str(customer.name),
            "customer.email": _safe_str(customer.email),
        }

        # Find all placeholders in the template
        placeholder_pattern = re.compile(r"\{([^\}]+)\}")
        placeholders = set(placeholder_pattern.findall(template))

        # Verify that every placeholder is allowed
        disallowed = placeholders - _ALLOWED_KEYS
        if disallowed:
            raise ValueError(f"Template contains disallowed placeholders: {', '.join(disallowed)}")

        # Replace placeholders safely
        def replacer(match):
            key = match.group(1)
            return context.get(key, "")

        rendered = placeholder_pattern.sub(replacer, template)
        return rendered

    except Exception as exc:
        # Do not leak sensitive information in the error message
        raise ValueError("Failed to generate receipt") from exc