import re
from typing import Dict, Any

# ------------------------------------------------------------------
# Dummy data models (replace with real ORM / database access in prod)
# ------------------------------------------------------------------

class Customer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


class Order:
    def __init__(self, order_id: str, total: float, customer: Customer):
        self.order_id = order_id
        self.total = total
        self.customer = customer


# In‑memory registry for demo purposes – replace with real DB calls
_order_registry: Dict[str, Order] = {}


def register_order(order: Order) -> None:
    """Register an order in the in‑memory registry."""
    _order_registry[order.order_id] = order


def get_order_by_id(order_id: str) -> Order:
    """Retrieve an order by ID or raise KeyError."""
    return _order_registry[order_id]


# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------

PLACEHOLDER_PATTERN = re.compile(r"\{([a-zA-Z_][\w\.]*)\}")

# Whitelist of attributes that are safe to expose in the receipt
ALLOWED_ORDER_ATTRS = {
    "order_id",
    "total",
}
ALLOWED_CUSTOMER_ATTRS = {
    "name",
    "email",
}


def _resolve_placeholder(order: Order, key: str) -> Any:
    """
    Resolve a single placeholder key against an order and its customer.
    Raises ValueError if the key is not allowed or does not exist.
    """
    # Split by dot to support nested attributes
    parts = key.split(".")
    if not parts:
        raise ValueError(f"Empty placeholder")

    # Resolve order attributes
    obj = order
    for i, part in enumerate(parts):
        if isinstance(obj, Order) and part == "customer":
            obj = order.customer
            continue

        if isinstance(obj, Order):
            allowed_attrs = ALLOWED_ORDER_ATTRS
        elif isinstance(obj, Customer):
            allowed_attrs = ALLOWED_CUSTOMER_ATTRS
        else:
            raise ValueError(f"Unsupported object type for placeholder '{key}'")

        if part not in allowed_attrs:
            raise ValueError(f"Access to disallowed attribute '{part}' in placeholder '{key}'")

        try:
            obj = getattr(obj, part)
        except AttributeError as exc:
            raise ValueError(f"Attribute '{part}' not found for placeholder '{key}'") from exc

    return obj


def generate_customer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order ID using the supplied template.
    Placeholders in the template like '{order.total}' or '{customer.name}'
    are replaced with actual values from the order and customer objects.

    Raises:
        ValueError: If the order cannot be found, a placeholder is invalid,
                    or access to sensitive data is attempted.
    """
    # Validate inputs
    if not isinstance(order_id, str) or not order_id.strip():
        raise ValueError("order_id must be a non-empty string")
    if not isinstance(template, str):
        raise ValueError("template must be a string")

    # Retrieve the order (this may involve I/O; ensure it is safely handled)
    try:
        order = get_order_by_id(order_id)
    except KeyError as exc:
        raise ValueError(f"Order with ID '{order_id}' not found") from exc

    # Find all placeholders
    placeholders = PLACEHOLDER_PATTERN.findall(template)

    # Resolve each placeholder and build a mapping for str.format
    resolved: Dict[str, Any] = {}
    for ph in placeholders:
        if ph in resolved:
            continue  # already resolved
        value = _resolve_placeholder(order, ph)
        resolved[ph] = value

    # Perform the substitution
    try:
        receipt = template.format(**resolved)
    except KeyError as exc:
        # This should not happen because we pre-resolved all placeholders
        raise ValueError(f"Missing value for placeholder '{exc.args[0]}'") from exc
    except Exception as exc:
        # Catch any formatting errors (e.g., type issues)
        raise ValueError(f"Failed to format receipt: {exc}") from exc

    return receipt


# ------------------------------------------------------------------
# Example usage (for testing purposes only)
# ------------------------------------------------------------------

if __name__ == "__main__":
    # Create sample data
    cust = Customer(name="Alice Smith", email="alice@example.com")
    order = Order(order_id="ORD123", total=199.99, customer=cust)
    register_order(order)

    tmpl = (
        "Receipt for Order {order_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total:.2f}\n"
        "Thank you for shopping with us!"
    )

    print(generate_customer_receipt("ORD123", tmpl))