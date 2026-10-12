import re
from typing import Any, Dict

# Assume these classes are defined elsewhere in the project.
# They are imported here for type checking purposes only.
try:
    from ecommerce.models import Order, User  # noqa: F401
except ImportError:  # pragma: no cover
    class User:
        def __init__(self, name: str, email: str):
            self.name = name
            self.email = email

    class Order:
        def __init__(self, order_id: str, total: float, customer: User):
            self.id = order_id
            self.total = total
            self.customer = customer

        @staticmethod
        def get_by_id(order_id: str) -> "Order | None":
            """Placeholder for actual DB lookup."""
            return None


# Restricted attributes that should not be exposed in the receipt.
RESTRICTED_ATTRIBUTES = {"email", "ssn", "credit_card_number"}


def _resolve_attribute(obj: Any, attr_path: str) -> Any:
    """
    Resolve a dotted attribute path on an object.
    Raises ValueError if any part of the path is restricted.
    """
    parts = attr_path.split(".")
    current = obj
    for part in parts:
        if part in RESTRICTED_ATTRIBUTES:
            raise ValueError(f"Attempt to access restricted attribute: {part}")
        try:
            current = getattr(current, part)
        except AttributeError as exc:  # pragma: no cover
            raise ValueError(f"Attribute path '{attr_path}' not found") from exc
    return current


def create_user_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string by filling placeholders in the provided template
    with data from the order and its customer.

    Parameters:
        order_id (str): The unique identifier of the order.
        template (str): Receipt template containing placeholders like
                        '{customer.name}', '{order.total}'.

    Returns:
        str: The formatted receipt string.

    Raises:
        ValueError: If the order ID is invalid or if a restricted attribute
                    is referenced in the template.
    """
    # Fetch order; raise if not found.
    order = Order.get_by_id(order_id)
    if not order:
        raise ValueError(f"Invalid order ID: {order_id}")

    # Find all placeholders in the template.
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    placeholders = placeholder_pattern.findall(template)

    # Build a mapping of placeholder names to their resolved values.
    context: Dict[str, Any] = {}
    for key in placeholders:
        # Determine the base object (order or customer) and attribute path.
        if key.startswith("customer."):
            obj = order.customer
            attr_path = key[len("customer.") :]
        elif key.startswith("order."):
            obj = order
            attr_path = key[len("order.") :]
        else:
            raise ValueError(f"Unsupported placeholder: {key}")

        # Resolve the attribute safely.
        value = _resolve_attribute(obj, attr_path)
        context[key] = value

    # Perform the substitution. Use a custom format mapping to allow
    # placeholders like '{customer.name}'.
    class SafeMapping(dict):
        def __missing__(self, key: str) -> Any:
            # If a placeholder was not resolved earlier, raise an error.
            raise ValueError(f"Missing value for placeholder: {key}")

    try:
        formatted = template.format(**SafeMapping(context))
    except KeyError as exc:  # pragma: no cover
        raise ValueError(f"Missing placeholder value for {exc}") from exc

    return formatted