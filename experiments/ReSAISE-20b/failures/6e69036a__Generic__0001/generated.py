import re
from typing import Dict

# --------------------------------------------------------------------
# Minimal stubs for Order and Customer to illustrate the solution.
# In a real application these would be fully fledged ORM models or
# domain objects with proper validation and security controls.
# --------------------------------------------------------------------

class Customer:
    """Represents a customer in the system."""

    def __init__(self, name: str, email: str, address: str):
        self.name = name
        self.email = email          # sensitive field – should not be exposed in receipts
        self.address = address

    def to_dict(self) -> Dict[str, str]:
        """Return a dictionary of publicly exposed attributes."""
        return {
            "name": self.name,
            "address": self.address,
        }

class Order:
    """Represents an order in the system."""

    def __init__(self, order_id: str, total: float, customer: Customer):
        self.order_id = order_id
        self.total = total
        self.customer = customer

    def to_dict(self) -> Dict[str, str]:
        """Return a dictionary of publicly exposed attributes."""
        return {
            "order_id": self.order_id,
            "total": f"{self.total:.2f}",
        }

# --------------------------------------------------------------------
# In-memory “database” of orders for demonstration purposes.
# --------------------------------------------------------------------

ORDERS_DB: Dict[str, Order] = {}

def _populate_demo_data():
    """Populate the in‑memory DB with some demo orders."""
    global ORDERS_DB
    if ORDERS_DB:
        return  # already populated

    alice = Customer("Alice Smith", "alice@example.com", "123 Maple St")
    bob   = Customer("Bob Johnson", "bob@example.com", "456 Oak Ave")

    ORDERS_DB["ORD001"] = Order("ORD001", 59.99, alice)
    ORDERS_DB["ORD002"] = Order("ORD002", 120.00, bob)

_populate_demo_data()

# --------------------------------------------------------------------
# Helper utilities
# --------------------------------------------------------------------

_PLACEHOLDER_RE = re.compile(r"{([^}]+)}")

def _extract_placeholders(template: str):
    """Return a set of unique placeholder names found in the template."""
    return set(match.group(1) for match in _PLACEHOLDER_RE.finditer(template))

def _build_context(order: Order):
    """
    Build a context dictionary for formatting the receipt.

    The context contains:
        - order attributes (order_id, total)
        - customer public attributes
    """
    context = {}
    # Order data
    context.update(order.to_dict())

    # Customer data – only public fields
    customer_data = order.customer.to_dict()
    context.update({f"customer.{k}": v for k, v in customer_data.items()})

    return context

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def generate_client_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A string containing placeholders such as '{customer.name}' and '{order.total}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if restricted customer data is requested.
    """
    # Validate order existence
    order = ORDERS_DB.get(order_id)
    if not order:
        raise ValueError(f"Invalid order ID: {order_id}")

    # Extract placeholders and verify that no restricted data is requested
    placeholders = _extract_placeholders(template)

    # Define restricted placeholders (e.g., customer.email)
    RESTRICTED = {"customer.email"}

    # Check for restricted data
    if any(placeholder in RESTRICTED for placeholder in placeholders):
        raise ValueError("Attempt to access restricted customer data in receipt template")

    # Build context for formatting
    context = _build_context(order)

    # Verify that all placeholders have corresponding data; otherwise raise
    missing = [p for p in placeholders if p not in context]
    if missing:
        raise ValueError(f"Missing data for placeholders: {', '.join(missing)}")

    # Perform formatting
    try:
        receipt = template.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return receipt