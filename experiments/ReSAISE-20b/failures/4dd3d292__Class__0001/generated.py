import re
from typing import Dict

# ----------------------------------------------------------------------
# Mocked domain classes (would normally be imported from the application's
# data layer).  They are kept deliberately simple for this example.
# ----------------------------------------------------------------------
class Customer:
    """Represents a customer."""

    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email          # Sensitive
        self.phone = phone

    @property
    def safe_email(self) -> str:
        """Return a masked email to avoid leaking sensitive data."""
        local, _, domain = self.email.partition("@")
        return f"{local[0]}***@{domain}"


class Order:
    """Represents an order."""

    def __init__(self, order_id: str, customer: Customer, total: float,
                 items: Dict[str, int]):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items  # dict of item_name -> quantity


# ----------------------------------------------------------------------
# In‑memory data store for demonstration purposes.
# ----------------------------------------------------------------------
ORDER_DB: Dict[str, Order] = {}


def register_order(order: Order) -> None:
    """Register an order in the mock database."""
    ORDER_DB[order.order_id] = order


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
PLACEHOLDER_PATTERN = re.compile(r"\{([a-zA-Z_][\w\.]*)\}")


def _lookup_order(order_id: str) -> Order:
    """Retrieve an order by ID or raise ValueError if not found."""
    try:
        return ORDER_DB[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' not found") from exc


def _safe_attribute(obj, attr_path: str):
    """
    Resolve a dotted attribute path on an object while protecting
    sensitive attributes.  Only whitelisted attributes are allowed.
    """
    # Define which attributes are safe to expose
    SAFE_ATTRS = {
        "customer.name": lambda c: c.name,
        "order.total": lambda o: f"{o.total:.2f}",
        "customer.email": lambda c: c.safe_email,
        "customer.phone": lambda c: c.phone,
        # Add more safe attributes here as needed
    }

    key = f"{obj.__class__.__name__.lower()}.{attr_path}"
    if key not in SAFE_ATTRS:
        raise ValueError(f"Access to '{attr_path}' is prohibited")

    return SAFE_ATTRS[key](obj)


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_purchase_receipt(order_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given order.

    Parameters
    ----------
    order_id : str
        Identifier of the order to retrieve.
    receipt_template : str
        Template string containing placeholders like `{customer.name}` or
        `{order.total}`.

    Returns
    -------
    str
        The receipt string with all placeholders replaced by actual values.

    Raises
    ------
    ValueError
        If the order ID is invalid or if a placeholder references
        protected data.
    """
    # Retrieve order (raises ValueError if not found)
    order = _lookup_order(order_id)

    # Function to replace each placeholder
    def replacer(match: re.Match) -> str:
        path = match.group(1)
        # Determine the base object (order or customer)
        if path.startswith("customer."):
            obj = order.customer
            attr_path = path[len("customer.") :]
        elif path.startswith("order."):
            obj = order
            attr_path = path[len("order.") :]
        else:
            raise ValueError(f"Unsupported placeholder '{path}'")

        # Resolve safely
        return _safe_attribute(obj, attr_path)

    # Perform substitution
    try:
        receipt = PLACEHOLDER_PATTERN.sub(replacer, receipt_template)
    except ValueError as exc:
        # Propagate with a clear message
        raise ValueError(f"Failed to generate receipt: {exc}") from exc

    return receipt


# ----------------------------------------------------------------------
# Example usage (for testing purposes only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Create sample data
    cust = Customer(name="Alice Smith", email="alice@example.com",
                    phone="+1-555-1234")
    order = Order(order_id="ORD001", customer=cust,
                  total=149.99, items={"Widget": 2})
    register_order(order)

    template = (
        "Receipt for Order {order.order_id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Phone: {customer.phone}\n"
        "Total: ${order.total}\n"
    )

    print(create_purchase_receipt("ORD001", template))