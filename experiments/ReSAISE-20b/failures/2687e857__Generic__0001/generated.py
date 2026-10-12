import re
from typing import Any, Dict

# Assume these classes are defined elsewhere in the application.
# They are imported here for type checking purposes only.
try:
    from ecommerce.models import Order, Customer  # noqa: F401
except ImportError:  # pragma: no cover
    # Minimal stubs for type checking / testing purposes.
    class Customer:
        def __init__(self, name: str, email: str):
            self.name = name
            self.email = email

    class Order:
        def __init__(self, order_id: str, total: float, customer: Customer):
            self.order_id = order_id
            self.total = total
            self.customer = customer

        @staticmethod
        def get_by_id(order_id: str) -> "Order":
            """Stub method – replace with actual DB lookup."""
            raise NotImplementedError("Replace with database access logic.")


def _safe_getattr(obj: Any, attr: str) -> Any:
    """
    Safely retrieve an attribute from an object.
    Raises ValueError if the attribute is protected (starts with '_')
    or does not exist.
    """
    if attr.startswith("_"):
        raise ValueError(f"Attempted to access protected attribute '{attr}'.")
    if not hasattr(obj, attr):
        raise ValueError(f"Attribute '{attr}' does not exist on object of type {type(obj).__name__}.")
    return getattr(obj, attr)


def _replace_placeholders(template: str, context: Dict[str, Any]) -> str:
    """
    Replace placeholders in the form {path.to.attribute} with values from context.
    """
    pattern = re.compile(r"\{([^{}]+)\}")

    def replacer(match: re.Match) -> str:
        path = match.group(1).strip()
        parts = path.split(".")
        if not parts:
            return match.group(0)

        # Resolve the root object
        obj = context.get(parts[0])
        if obj is None:
            raise ValueError(f"Unknown placeholder root '{parts[0]}' in template.")
        # Walk through remaining attributes
        for attr in parts[1:]:
            obj = _safe_getattr(obj, attr)
        # Convert to string for insertion
        return str(obj)

    return pattern.sub(replacer, template)


def create_transaction_receipt(transaction_id: str, temp_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the provided template.

    Parameters
    ----------
    transaction_id : str
        The identifier of the order.
    temp_format : str
        A template string containing placeholders such as '{customer.name}' or '{order.total}'.

    Returns
    -------
    str
        The formatted receipt string with all placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the transaction_id is invalid or if a placeholder references protected data.
    """
    # Retrieve the order; raise ValueError if not found
    try:
        order = Order.get_by_id(transaction_id)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Invalid transaction ID '{transaction_id}'.") from exc

    if not isinstance(order, Order):
        raise ValueError(f"Object retrieved for ID '{transaction_id}' is not an Order instance.")

    # Build context mapping root names to objects
    context = {
        "order": order,
        "customer": order.customer,
    }

    # Perform placeholder replacement
    receipt = _replace_placeholders(temp_format, context)
    return receipt