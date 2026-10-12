import re
from typing import Any

# The Order and Customer classes are assumed to exist in the environment.
# They should expose public attributes that can be accessed via getattr.

PLACEHOLDER_PATTERN = re.compile(r"\{([a-zA-Z_][\w\.]*)\}")

def _resolve_attribute(obj: Any, attr_path: str) -> Any:
    """
    Resolve a dotted attribute path on an object safely.
    Only public attributes (not starting with underscore) are allowed.
    """
    parts = attr_path.split(".")
    for part in parts:
        if part.startswith("_"):
            raise ValueError(f"Access to private attribute '{part}' is forbidden.")
        try:
            obj = getattr(obj, part)
        except AttributeError as exc:
            raise ValueError(f"Attribute '{part}' not found on object of type {type(obj).__name__}") from exc
    return obj

def generate_customer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order ID using the provided template.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A string containing placeholders like '{order.total}' or '{customer.name}'
        that will be replaced with actual data.

    Returns
    -------
    str
        The fully rendered receipt string.

    Raises
    ------
    ValueError
        If the order cannot be found, if a placeholder refers to an invalid or private attribute,
        or if any other error occurs during rendering.
    """
    # Retrieve the order object.  In a real system this might query a database.
    try:
        # Assume `get_order_by_id` is a function provided by the system
        order = get_order_by_id(order_id)  # type: ignore[name-defined]
    except Exception as exc:
        raise ValueError(f"Unable to retrieve order with ID '{order_id}'") from exc

    # The order is expected to have a reference to its customer
    try:
        customer = getattr(order, "customer")
    except AttributeError as exc:
        raise ValueError(f"Order '{order_id}' does not contain a customer reference") from exc

    # Build a mapping for quick lookup during substitution
    def placeholder_replacer(match: re.Match) -> str:
        path = match.group(1)
        try:
            if path.startswith("order."):
                value = _resolve_attribute(order, path[len("order.") :])
            elif path.startswith("customer."):
                value = _resolve_attribute(customer, path[len("customer.") :])
            else:
                raise ValueError(f"Unsupported placeholder prefix in '{path}'")
        except Exception as exc:
            raise ValueError(f"Error resolving placeholder '{{{path}}}'") from exc
        return str(value)

    try:
        receipt = PLACEHOLDER_PATTERN.sub(placeholder_replacer, template)
    except Exception as exc:
        raise ValueError("Failed to render receipt") from exc

    return receipt