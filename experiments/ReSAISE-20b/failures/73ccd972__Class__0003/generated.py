import re
from typing import Any, Dict

# ------------------------------------------------------------------
# Mock data structures (in a real system these would come from the DB)
# ------------------------------------------------------------------

class Customer:
    def __init__(self, name: str, email: str, phone: str,
                 address: str, ssn: str = None):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.ssn = ssn  # sensitive


class Order:
    def __init__(self, order_id: str, customer: Customer,
                 total: float, items: list):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items  # list of dicts with 'name', 'qty', 'price'


# Simulated in‑memory store
ORDERS_DB: Dict[str, Order] = {}


def get_order_by_id(order_id: str) -> Order | None:
    """Retrieve an order from the simulated store."""
    return ORDERS_DB.get(order_id)


# ------------------------------------------------------------------
# Receipt rendering
# ------------------------------------------------------------------

# Define the set of safe attributes that can be referenced in a template.
ALLOWED_PATHS = {
    "customer.name",
    "customer.email",
    "customer.phone",
    "customer.address",
    "order.total",
    "order.items",
    # add more safe paths as required
}


def _resolve_path(obj: Any, path: str) -> Any:
    """
    Resolve a dotted attribute path on an object.
    For example, 'customer.name' on an Order instance returns the name string.
    """
    attrs = path.split(".")
    current = obj
    for attr in attrs:
        if not hasattr(current, attr):
            raise AttributeError(f"Attribute '{attr}' not found.")
        current = getattr(current, attr)
    return current


def _render_template(template: str, context: Dict[str, Any]) -> str:
    """
    Replace placeholders in the form {path} with their corresponding values.
    Only paths listed in ALLOWED_PATHS are permitted.
    """
    pattern = re.compile(r"\{([^{}]+)\}")

    def replacer(match: re.Match) -> str:
        path = match.group(1).strip()
        if path not in ALLOWED_PATHS:
            raise ValueError(f"Restricted or unknown placeholder: '{path}'")
        value = _resolve_path(context, path)
        # Convert non‑string values to string in a safe manner
        if isinstance(value, list):
            # Render lists as comma‑separated strings of item names
            return ", ".join(str(item) for item in value)
        return str(value)

    return pattern.sub(replacer, template)


def create_order_receipt(purchase_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given order.

    Parameters
    ----------
    purchase_id : str
        Unique identifier of the order.
    receipt_template : str
        Template containing placeholders like `{customer.name}`.

    Returns
    -------
    str
        The receipt string with all placeholders substituted.

    Raises
    ------
    ValueError
        If the order does not exist or if a placeholder references
        restricted data.
    """
    # 1. Retrieve the order
    order = get_order_by_id(purchase_id)
    if not order:
        raise ValueError(f"Order ID '{purchase_id}' does not exist.")

    # 2. Prepare context for rendering
    context = {
        "order": order,
        "customer": order.customer,
    }

    # 3. Render the template safely
    try:
        receipt = _render_template(receipt_template, context)
    except AttributeError as exc:
        # Raised when a non‑existent attribute is referenced
        raise ValueError(f"Invalid placeholder: {exc}") from exc
    except ValueError as exc:
        # Raised for restricted placeholders or other validation errors
        raise

    return receipt


# ------------------------------------------------------------------
# Example usage (this part would normally be in a separate test module)
# ------------------------------------------------------------------

if __name__ == "__main__":
    # Create sample data
    cust = Customer(
        name="Jane Doe",
        email="jane.doe@example.com",
        phone="+1-555-1234",
        address="123 Elm Street, Springfield",
        ssn="123-45-6789",  # should not be exposed
    )
    order = Order(
        order_id="ORD-001",
        customer=cust,
        total=149.99,
        items=[
            {"name": "Wireless Mouse", "qty": 1, "price": 29.99},
            {"name": "Keyboard", "qty": 1, "price": 119.99},
        ],
    )
    ORDERS_DB[order.order_id] = order

    template = (
        "Receipt for Order {order.order_id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Total: ${order.total:.2f}\n"
        "Items: {order.items}"
    )

    try:
        print(create_order_receipt("ORD-001", template))
    except ValueError as e:
        print(f"Error: {e}")