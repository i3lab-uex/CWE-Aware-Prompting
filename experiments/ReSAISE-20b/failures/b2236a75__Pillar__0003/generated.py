import re
from typing import Any, Dict

# --------------------------------------------------------------------
# Assume the following data model classes exist in the application.
# They are represented here only for type‑checking and documentation
# purposes. In a real code base they would be imported from the
# appropriate modules.
# --------------------------------------------------------------------
class Customer:
    """Customer data model."""
    # Example attributes (the actual class may contain many more)
    name: str
    email: str
    phone: str
    # Sensitive attributes that must not be exposed via receipts.
    password_hash: str  # <-- sensitive


class Order:
    """Order data model."""
    # Example attributes
    id: str
    total: float
    status: str
    customer: Customer

    @classmethod
    def get_by_id(cls, order_id: str) -> "Order":
        """Retrieve an Order instance by its ID."""
        # In the real system this would query a database.
        raise NotImplementedError


# --------------------------------------------------------------------
# Utility functions
# --------------------------------------------------------------------
def _get_attr_chain(obj: Any, chain: str) -> Any:
    """
    Safely traverse an attribute chain on *obj*.

    Parameters
    ----------
    obj : Any
        The root object (e.g. an Order instance).
    chain : str
        Attribute path separated by dots, e.g. "customer.name".

    Returns
    -------
    Any
        The value of the final attribute.

    Raises
    ------
    ValueError
        If any part of the chain is missing or points to a disallowed attribute.
    """
    parts = chain.split(".")
    current = obj
    for part in parts:
        # Disallow access to private or sensitive attributes.
        if part.startswith("_"):
            raise ValueError(f"Access to private attribute '{part}' is forbidden.")
        # Optionally, disallow specific sensitive attributes.
        if isinstance(current, Customer) and part == "password_hash":
            raise ValueError("Access to customer password hash is forbidden.")
        try:
            current = getattr(current, part)
        except AttributeError as exc:
            raise ValueError(f"Attribute '{part}' not found on {type(current).__name__}") from exc
    return current


# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def generate_customer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for an order.

    Parameters
    ----------
    order_id : str
        Identifier of the order to process.
    template : str
        Receipt template containing placeholders in the form '{order.attr}'
        or '{customer.attr}'.

    Returns
    -------
    str
        The formatted receipt string with all placeholders replaced by actual values.

    Raises
    ------
    ValueError
        If the order cannot be found, if placeholder resolution fails,
        or if an attempt is made to access sensitive data.
    """
    # Retrieve the order object; raise ValueError if not found.
    try:
        order = Order.get_by_id(order_id)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Order with ID '{order_id}' could not be retrieved") from exc

    # Pre‑populate a dictionary of context objects for quick lookup.
    context: Dict[str, Any] = {
        "order": order,
        "customer": getattr(order, "customer", None),
    }

    # Regular expression to find placeholders like {order.total}
    placeholder_pattern = re.compile(r"\{([a-zA-Z_][\w\.]*)\}")

    def replace_match(match: re.Match) -> str:
        key = match.group(1)
        # Split the key into root and attribute chain
        if "." not in key:
            raise ValueError(f"Invalid placeholder '{{{key}}}' – missing attribute chain.")
        root, attr_chain = key.split(".", 1)
        if root not in context or context[root] is None:
            raise ValueError(f"Context object '{root}' not available for placeholder '{{{key}}}'.")
        try:
            value = _get_attr_chain(context[root], attr_chain)
        except ValueError as exc:
            raise ValueError(f"Failed to resolve placeholder '{{{key}}}': {exc}") from exc
        # Convert the value to string for insertion.
        return str(value)

    try:
        receipt = placeholder_pattern.sub(replace_match, template)
    except ValueError as exc:  # pragma: no cover
        raise

    return receipt