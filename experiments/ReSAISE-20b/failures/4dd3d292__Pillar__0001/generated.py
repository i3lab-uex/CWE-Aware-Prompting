import re
from typing import Dict, Any

# --------------------------------------------------------------------------- #
#  Dummy data structures – in a real system these would be provided by the
#  application's domain layer or ORM. They are included here only to make the
#  example self‑contained and testable.
# --------------------------------------------------------------------------- #
class Customer:
    def __init__(self, name: str, email: str, _ssn: str = None):
        self.name = name
        self.email = email
        # Protected attribute – should never be exposed via the receipt template
        self._ssn = _ssn


class Order:
    def __init__(self, order_id: str, customer: Customer, total: float,
                 items: Dict[str, int]):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items  # e.g., {"widget": 3, "gadget": 1}

    def __repr__(self) -> str:
        return f"<Order {self.order_id}>"


# --------------------------------------------------------------------------- #
#  In‑memory "database" of orders – in production this would be replaced by
#  a persistent store or an ORM query.
# --------------------------------------------------------------------------- #
ORDER_DB: Dict[str, Order] = {}


def register_order(order: Order) -> None:
    """Register an order in the in‑memory store."""
    ORDER_DB[order.order_id] = order


# --------------------------------------------------------------------------- #
#  Core functionality – create_purchase_receipt
# --------------------------------------------------------------------------- #
PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_.]+)\}")


def _resolve_placeholder(path: str, context: Any) -> str:
    """
    Resolve a dotted attribute path against the given context object.
    Raises ValueError if an attempt is made to access a protected attribute
    (starting with an underscore) or if the path cannot be resolved.
    """
    parts = path.split(".")
    obj = context
    for part in parts:
        # Protect against accessing protected attributes.
        if part.startswith("_"):
            raise ValueError(f"Access to protected attribute '{part}' is forbidden")
        try:
            obj = getattr(obj, part)
        except AttributeError as exc:
            raise ValueError(f"Invalid placeholder '{path}': {exc}") from exc

    # If the final value is a callable (e.g., method), call it
    if callable(obj):
        obj = obj()

    # Convert to string for insertion into the template
    return str(obj)


def create_purchase_receipt(order_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt string for the given order ID.

    Parameters
    ----------
    order_id : str
        Identifier of the order to be processed.
    receipt_template : str
        Template string containing placeholders such as '{customer.name}'
        and '{order.total}'.

    Returns
    -------
    str
        The receipt string with all placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the order ID does not exist or if a placeholder attempts to
        access protected information.
    """
    # 1. Retrieve the order – raise if not found
    order = ORDER_DB.get(order_id)
    if order is None:
        raise ValueError(f"Order ID '{order_id}' not found")

    # 2. Prepare a context mapping for placeholder resolution
    context = {
        "order": order,
        "customer": order.customer,
    }

    # 3. Resolve all placeholders in the template
    def replace_match(match: re.Match) -> str:
        placeholder = match.group(1)
        return _resolve_placeholder(placeholder, context)

    try:
        receipt = PLACEHOLDER_RE.sub(replace_match, receipt_template)
    except ValueError as exc:
        # Propagate the error to signal template misuse
        raise exc

    return receipt


# --------------------------------------------------------------------------- #
#  Example usage – this section can be removed or commented out in production.
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Create a sample customer and order
    cust = Customer(name="Alice Smith", email="alice@example.com")
    ord_ = Order(order_id="ORD12345",
                 customer=cust,
                 total=99.95,
                 items={"widget": 2, "gadget": 1})
    register_order(ord_)

    template = (
        "Receipt for Order {order.order_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total:.2f}\n"
        "Items:\n"
        "{items}"
    )

    # Since the template contains a placeholder 'items' that is not directly
    # available in the context, we extend the context before formatting.
    # In a real implementation you might provide helper functions or
    # custom formatters for such cases.
    context = {
        "order": ord_,
        "customer": cust,
        "items": "\n".join(f" - {k}: {v}" for k, v in ord_.items.items()),
    }

    # Use a simple manual substitution to handle the custom 'items' placeholder
    receipt = template.format(**context)
    print(receipt)