import re
from typing import Dict

# --------------------------------------------------------------------
# The following classes are assumed to be part of the application
# and provide access to order and customer data.  They are included
# here as minimal stubs for demonstration purposes only.
# --------------------------------------------------------------------

class Customer:
    """
    Represents a customer. Only a subset of attributes are considered
    safe for inclusion in a public receipt.
    """
    __restricted_attrs__ = {"ssn", "credit_card_number"}

    def __init__(self, name: str, email: str, ssn: str = None,
                 credit_card_number: str = None):
        self.name = name
        self.email = email
        self.ssn = ssn
        self.credit_card_number = credit_card_number


class Order:
    """
    Represents an order.  Only a subset of attributes are considered
    safe for inclusion in a public receipt.
    """
    __restricted_attrs__ = {"payment_method", "billing_address"}

    def __init__(self, order_id: str, customer: Customer,
                 total: float, payment_method: str = None,
                 billing_address: str = None):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.payment_method = payment_method
        self.billing_address = billing_address


# --------------------------------------------------------------------
# Simulated data store (for demonstration).  In a real application
# this would be replaced by database queries or an ORM.
# --------------------------------------------------------------------
_ORDER_DB: Dict[str, Order] = {}


def _load_demo_data():
    """Populate the in-memory order database with a single example."""
    global _ORDER_DB
    cust = Customer(name="Alice Smith", email="alice@example.com",
                    ssn="123-45-6789", credit_card_number="4111111111111111")
    order = Order(order_id="ORD-001", customer=cust,
                  total=129.99, payment_method="VISA",
                  billing_address="123 Main St")
    _ORDER_DB[order.order_id] = order


# Load demo data at module import
_load_demo_data()


def _get_order(order_id: str) -> Order:
    """Retrieve an order by ID or raise ValueError if not found."""
    try:
        return _ORDER_DB[order_id]
    except KeyError as exc:
        raise ValueError(f"Invalid order ID: {order_id}") from exc


# --------------------------------------------------------------------
# Helper functions for safe placeholder resolution
# --------------------------------------------------------------------

_ALLOWED_PLACEHOLDERS = {
    "customer.name",
    "customer.email",
    "order.total",
    "order.order_id"
}

_PLACEHOLDER_PATTERN = re.compile(r"\{([^\}]+)\}")


def _validate_placeholders(template: str):
    """
    Ensure that the template only contains allowed placeholders.
    Raises ValueError if a disallowed placeholder is found.
    """
    for match in _PLACEHOLDER_PATTERN.finditer(template):
        key = match.group(1)
        if key not in _ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Disallowed placeholder: {{{key}}}")


def _build_context(order: Order) -> Dict[str, str]:
    """
    Build a mapping from placeholder keys to string values.
    Only includes safe attributes.
    """
    return {
        "customer.name": order.customer.name,
        "customer.email": order.customer.email,
        "order.total": f"{order.total:.2f}",
        "order.order_id": order.order_id,
    }


# --------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------

def generate_client_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt for the given order ID using the supplied template.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A string containing placeholders such as `{customer.name}` and
        `{order.total}`.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if the template contains a
        placeholder that would expose restricted data.
    """
    # Retrieve order and validate existence
    order = _get_order(order_id)

    # Validate that the template does not request restricted data
    _validate_placeholders(template)

    # Build context mapping
    ctx = _build_context(order)

    try:
        receipt = template.format(**ctx)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing placeholder data for {exc}") from exc

    return receipt


# --------------------------------------------------------------------
# Example usage (for testing purposes only)
# --------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.order_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total}\n"
    )
    print(generate_client_receipt("ORD-001", tmpl))