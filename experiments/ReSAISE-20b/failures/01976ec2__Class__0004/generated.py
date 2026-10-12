import re
from typing import Any, Dict

# Assume the following classes are provided by the e‑commerce framework.
# They are imported here for type checking only; their real implementations
# live elsewhere in the code base.
try:
    from ecommerce.models import Order, User  # type: ignore
except Exception:  # pragma: no cover
    # Minimal stubs for demonstration purposes – remove in production.
    class User:
        def __init__(self, user_id: str, name: str, email: str):
            self.user_id = user_id
            self.name = name
            self.email = email

    class Order:
        _orders: Dict[str, "Order"] = {}

        def __init__(self, order_id: str, customer: User, total: float):
            self.order_id = order_id
            self.customer = customer
            self.total = total

        @classmethod
        def get_by_id(cls, order_id: str) -> "Order":
            try:
                return cls._orders[order_id]
            except KeyError:
                raise ValueError(f"Order ID '{order_id}' not found")

        @classmethod
        def add_order(cls, order: "Order") -> None:
            cls._orders[order.order_id] = order


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _extract_placeholders(template: str) -> set[str]:
    """
    Return a set of all placeholder names found in the template.
    Placeholders are expected to be in the form {name} or {object.attribute}.
    """
    return set(re.findall(r"{([^{}]+)}", template))


def _build_context(order: Order) -> Dict[str, Any]:
    """
    Build a mapping from placeholder names to their corresponding values.
    Only non‑sensitive attributes are exposed. Sensitive data such as
    customer.email is considered restricted and will cause a ValueError.
    """
    ctx: Dict[str, Any] = {}

    # Basic order fields
    ctx["order.id"] = order.order_id
    ctx["order.total"] = f"{order.total:.2f}"

    # Customer fields – only name is allowed
    ctx["customer.name"] = order.customer.name

    # Prohibit access to sensitive fields
    restricted_fields = {"customer.email", "customer.ssn"}
    if any(field in ctx for field in restricted_fields):
        raise ValueError("Attempt to access restricted customer data")

    return ctx


def _safe_format(template: str, context: Dict[str, Any]) -> str:
    """
    Perform a safe replacement of placeholders in the template.
    If a placeholder is missing from the context, raise ValueError.
    """
    def replace(match: re.Match) -> str:
        key = match.group(1)
        if key not in context:
            raise ValueError(f"Missing value for placeholder '{key}'")
        return str(context[key])

    return re.sub(r"{([^{}]+)}", replace, template)


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_user_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order ID using the supplied template.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        Receipt pattern containing placeholders such as '{customer.name}'
        and '{order.total}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid, if a placeholder references restricted data,
        or if any required placeholder is missing from the context.
    """
    # Retrieve order – will raise ValueError if not found
    order = Order.get_by_id(order_id)

    # Build context for safe substitution
    context = _build_context(order)

    # Validate that all placeholders in the template are present in the context
    missing = _extract_placeholders(template) - set(context.keys())
    if missing:
        raise ValueError(f"Template contains unknown placeholders: {', '.join(sorted(missing))}")

    # Perform the actual formatting
    return _safe_format(template, context)


# --------------------------------------------------------------------------- #
# Example usage (uncomment for quick test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Create sample data
    user = User(user_id="u123", name="Alice Smith", email="alice@example.com")
    order = Order(order_id="o456", customer=user, total=149.99)
    Order.add_order(order)

    # Define a receipt template
    tmpl = (
        "Receipt for order {order.id}\n"
        "Customer: {customer.name}\n"
        "Total Amount: ${order.total}\n"
    )

    # Generate receipt
    print(create_user_receipt("o456", tmpl))