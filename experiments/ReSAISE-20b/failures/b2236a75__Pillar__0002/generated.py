import re
from typing import Any

# ------------------------------------------------------------------
# Minimal data model stubs – in a real system these would be
# replaced by the actual ORM or database access layer.
# ------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email
        self.phone = phone


class Order:
    _orders_db = {}

    def __init__(self, order_id: str, total: float, customer: Customer):
        self.id = order_id
        self.total = total
        self.customer = customer

    @classmethod
    def get_by_id(cls, order_id: str) -> "Order":
        """Retrieve an Order instance by its ID."""
        if order_id not in cls._orders_db:
            raise KeyError(f"Order {order_id} not found")
        return cls._orders_db[order_id]

    @classmethod
    def register(cls, order: "Order"):
        """Register an Order instance for later lookup."""
        cls._orders_db[order.id] = order


# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------
def _resolve_placeholder(obj: Any, path: str) -> Any:
    """
    Resolve a dotted attribute path on an object.
    Raises ValueError if the path is invalid or attempts to access
    a private/sensitive attribute.
    """
    # Disallow leading underscores (private attributes)
    if any(part.startswith("_") for part in path.split(".")):
        raise ValueError(f"Access to private attribute in placeholder '{path}' is forbidden")

    current = obj
    for part in path.split("."):
        try:
            current = getattr(current, part)
        except AttributeError as exc:
            raise ValueError(f"Invalid placeholder path '{path}': {exc}") from None
    return current


def _replace_placeholders(template: str, context: dict) -> str:
    """
    Replace all placeholders in the template using the provided context.
    Placeholders are of the form {path} where 'path' may contain dots
    to access nested attributes.
    """
    pattern = re.compile(r"\{([^{}]+)\}")

    def _replacement(match: re.Match) -> str:
        placeholder = match.group(1).strip()
        try:
            value = _resolve_placeholder(context, placeholder)
        except ValueError as exc:
            raise ValueError(f"Error resolving placeholder '{placeholder}': {exc}") from None
        return str(value)

    try:
        result = pattern.sub(_replacement, template)
    except ValueError as exc:
        raise
    return result


# ------------------------------------------------------------------
# Main API function
# ------------------------------------------------------------------
def generate_customer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order ID using the provided
    template. Placeholders in the form `{order.total}` or `{customer.name}`
    are replaced with actual data from the order and its customer.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        Receipt template containing placeholders.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order cannot be found, a placeholder is invalid,
        or an attempt is made to access sensitive information.
    """
    try:
        order = Order.get_by_id(order_id)
    except KeyError as exc:
        raise ValueError(f"Order not found: {order_id}") from None

    context = {"order": order, "customer": order.customer}

    try:
        receipt = _replace_placeholders(template, context)
    except ValueError as exc:
        # Re‑raise with a generic message to avoid leaking internal details
        raise ValueError(f"Failed to generate receipt: {exc}") from None

    return receipt


# ------------------------------------------------------------------
# Example usage (this would normally be in a separate test module)
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Setup example data
    cust = Customer(name="Alice Smith", email="alice@example.com", phone="555-1234")
    order = Order(order_id="ORD001", total=99.95, customer=cust)
    Order.register(order)

    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total}\n"
    )

    print(generate_customer_receipt("ORD001", tmpl))