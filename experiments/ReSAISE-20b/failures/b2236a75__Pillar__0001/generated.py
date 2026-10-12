import re
from typing import Any

# --------------------------------------------------------------------------- #
# Dummy data models (replace with real implementations in production)
# --------------------------------------------------------------------------- #

class Customer:
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email
        self.phone = phone

class Order:
    def __init__(self, order_id: str, total: float, customer: Customer):
        self.order_id = order_id
        self.total = total
        self.customer = customer

# --------------------------------------------------------------------------- #
# In‑memory store and lookup helpers (replace with database access in real code)
# --------------------------------------------------------------------------- #

_orders_db = {}

def add_order(order: Order) -> None:
    """Store an order in the dummy database."""
    _orders_db[order.order_id] = order

def get_order_by_id(order_id: str) -> Order:
    """Retrieve an order from the dummy database."""
    try:
        return _orders_db[order_id]
    except KeyError as exc:
        raise ValueError(f"Order with ID {order_id!r} not found") from exc

# --------------------------------------------------------------------------- #
# Receipt generation
# --------------------------------------------------------------------------- #

PLACEHOLDER_PATTERN = re.compile(r'{([^}]+)}')

def _resolve_placeholder(order: Order, placeholder: str) -> Any:
    """
    Resolve a single placeholder against an order instance.

    Allowed roots: 'order', 'customer'.
    The placeholder must be a dot‑separated path, e.g. 'order.total' or
    'customer.name'.
    """
    parts = placeholder.split('.')
    if not parts:
        raise ValueError(f"Empty placeholder in template: {placeholder!r}")

    root_name = parts[0]
    if root_name == 'order':
        current: Any = order
    elif root_name == 'customer':
        current = order.customer
    else:
        raise ValueError(f"Disallowed placeholder root: {root_name!r}")

    for attr in parts[1:]:
        try:
            current = getattr(current, attr)
        except AttributeError as exc:
            raise ValueError(
                f"Attribute {attr!r} not found while resolving "
                f"{placeholder!r}"
            ) from exc

    return current

def generate_customer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order ID using the supplied
    template.

    Parameters
    ----------
    order_id : str
        Identifier of the order to process.
    template : str
        Receipt template containing placeholders like `{order.total}` or
        `{customer.name}`.

    Returns
    -------
    str
        The rendered receipt string with all placeholders replaced.

    Raises
    ------
    ValueError
        If the order cannot be found, a placeholder is malformed,
        or an attempt is made to access disallowed data.
    """
    # Acquire the order (this may raise ValueError if not found)
    order = get_order_by_id(order_id)

    # Find all placeholders in the template
    placeholders = PLACEHOLDER_PATTERN.findall(template)

    # Build a mapping of placeholder -> resolved value
    resolved = {}
    for ph in placeholders:
        try:
            resolved[ph] = _resolve_placeholder(order, ph)
        except ValueError as exc:
            # Wrap and re‑raise to provide context
            raise ValueError(f"Error resolving placeholder {ph!r}") from exc

    # Perform the substitution safely
    try:
        receipt = template.format(**resolved)
    except KeyError as exc:
        # This should not happen because we pre‑resolved all placeholders,
        # but guard against any unexpected formatting issues.
        raise ValueError(f"Missing placeholder value for {exc}") from exc
    except Exception as exc:
        # Catch any other formatting errors
        raise ValueError(f"Template rendering failed: {exc}") from exc

    return receipt

# --------------------------------------------------------------------------- #
# Example usage (for demonstration; remove or guard under __main__ in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Create dummy data
    cust = Customer(name="Alice Smith", email="alice@example.com", phone="+123456789")
    ord1 = Order(order_id="ORD1001", total=199.99, customer=cust)
    add_order(ord1)

    tmpl = (
        "Receipt for Order {order.order_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total Amount: ${order.total:.2f}\n"
    )

    print(generate_customer_receipt("ORD1001", tmpl))