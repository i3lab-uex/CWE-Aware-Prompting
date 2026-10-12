import re
from dataclasses import dataclass, field
from typing import Dict, Any

# --------------------------------------------------------------------------- #
#   Domain model (simplified for demonstration purposes)                     #
# --------------------------------------------------------------------------- #

@dataclass
class Customer:
    """Represents a customer.  Certain attributes are considered protected."""
    name: str
    email: str
    address: str
    _ssn: str = field(repr=False)  # protected attribute, should not be exposed

    def __post_init__(self):
        if not isinstance(self._ssn, str) or len(self._ssn) != 9:
            raise ValueError("SSN must be a 9‑digit string")

@dataclass
class Order:
    """Represents an order."""
    id: str
    customer: Customer
    total: float
    items: list

# --------------------------------------------------------------------------- #
#   In‑memory store of orders (simulating a repository)                       #
# --------------------------------------------------------------------------- #

ORDERS: Dict[str, Order] = {}

def register_order(order: Order) -> None:
    """Adds an order to the in‑memory store."""
    ORDERS[order.id] = order

# --------------------------------------------------------------------------- #
#   Helper utilities                                                      #
# --------------------------------------------------------------------------- #

def _safe_getattr(obj: Any, attr_name: str) -> Any:
    """
    Retrieve an attribute safely.
    Raises ValueError if the attribute is protected (starts with '_').
    """
    if attr_name.startswith('_'):
        raise ValueError(f"Attempt to access protected attribute '{attr_name}'")
    if not hasattr(obj, attr_name):
        raise ValueError(f"Attribute '{attr_name}' does not exist on object of type {type(obj).__name__}")
    return getattr(obj, attr_name)

def _resolve_placeholder(match: re.Match) -> str:
    """
    Resolve a single placeholder of the form {object.attribute}.
    """
    full_path = match.group(1).strip()
    try:
        obj_name, attr_name = full_path.split('.', 1)
    except ValueError:
        raise ValueError(f"Invalid placeholder syntax: {{{full_path}}}")

    # Resolve the object reference
    if obj_name == 'customer':
        context_obj = _current_order.customer  # type: ignore
    elif obj_name == 'order':
        context_obj = _current_order  # type: ignore
    else:
        raise ValueError(f"Unknown placeholder object '{obj_name}'")

    # Retrieve the attribute safely
    value = _safe_getattr(context_obj, attr_name)
    return str(value)

# --------------------------------------------------------------------------- #
#   Core function: compose_invoice_template                               #
# --------------------------------------------------------------------------- #

def compose_invoice_template(invoice_id: str, receipt_format: str) -> str:
    """
    Generates a formatted invoice string for the given order ID.

    Parameters
    ----------
    invoice_id : str
        Identifier of the order.
    receipt_format : str
        Template string containing placeholders such as '{customer.name}' or
        '{order.total}'. Placeholders are replaced with the corresponding
        values from the order and its customer.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid, or if a placeholder attempts to access
        protected customer information.
    """
    global _current_order  # used by the placeholder resolver
    if invoice_id not in ORDERS:
        raise ValueError(f"Order ID '{invoice_id}' does not exist.")

    _current_order = ORDERS[invoice_id]  # type: ignore

    placeholder_pattern = re.compile(r'\{([^{}]+)\}')

    try:
        receipt = placeholder_pattern.sub(_resolve_placeholder, receipt_format)
    finally:
        # Clean up the global reference to avoid leaking state
        _current_order = None  # type: ignore

    return receipt


# --------------------------------------------------------------------------- #
#   Example usage (this block can be removed in production)                 #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Create a customer and order
    cust = Customer(
        name="Jane Doe",
        email="jane.doe@example.com",
        address="123 Maple Street, Anytown, USA",
        _ssn="123456789"
    )
    order = Order(
        id="INV-001",
        customer=cust,
        total=149.99,
        items=["Widget A", "Widget B"]
    )
    register_order(order)

    # Define a receipt template
    template = (
        "Invoice #{invoice_id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Address: {customer.address}\n"
        "Total: ${order.total:.2f}"
    )

    # Render the receipt
    try:
        print(compose_invoice_template("INV-001", template))
    except ValueError as e:
        print(f"Error generating receipt: {e}")