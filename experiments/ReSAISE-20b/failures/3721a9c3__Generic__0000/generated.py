import re
from dataclasses import dataclass
from typing import Dict, Any

# --------------------------------------------------------------------
# Mock data layer – in a real application this would interface with
# a database or external service.  The examples below are only for
# demonstration purposes.
# --------------------------------------------------------------------

@dataclass(frozen=True)
class Customer:
    """Represents a customer in the e‑commerce system."""
    id: str
    name: str
    email: str
    # Sensitive data – should not be exposed in a buyer receipt.
    ssn: str | None = None

@dataclass(frozen=True)
class Order:
    """Represents an order."""
    id: str
    customer_id: str
    total: float
    items: list[str]

# In‑memory data stores
CUSTOMERS: Dict[str, Customer] = {
    "c001": Customer(id="c001", name="Alice Smith", email="alice@example.com", ssn="123-45-6789"),
    "c002": Customer(id="c002", name="Bob Jones", email="bob@example.com"),
}

ORDERS: Dict[str, Order] = {
    "o100": Order(id="o100", customer_id="c001", total=150.75, items=["Book", "Pen"]),
    "o101": Order(id="o101", customer_id="c002", total=42.00, items=["Notebook"]),
}

# --------------------------------------------------------------------
# Helper utilities
# --------------------------------------------------------------------

class RestrictedAccessError(ValueError):
    """Raised when an attempt is made to expose restricted data."""
    pass

def _get_order(order_id: str) -> Order:
    """Retrieve an order by its ID, raising ValueError if not found."""
    order = ORDERS.get(order_id)
    if order is None:
        raise ValueError(f"Order ID '{order_id}' does not exist.")
    return order

def _get_customer(customer_id: str) -> Customer:
    """Retrieve a customer by its ID, raising ValueError if not found."""
    customer = CUSTOMERS.get(customer_id)
    if customer is None:
        raise ValueError(f"Customer ID '{customer_id}' does not exist.")
    return customer

def _sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new dictionary that excludes keys containing sensitive
    information.  For this example we consider any key ending with 'ssn'
    as sensitive.
    """
    return {k: v for k, v in data.items() if not k.lower().endswith("ssn")}

# --------------------------------------------------------------------
# Core function
# --------------------------------------------------------------------

def generate_buyer_receipt(order_id: str, template: str) -> str:
    """
    Generate a buyer‑side receipt by filling placeholders in *template*
    with data from the order and its associated customer.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A format string containing placeholders such as '{customer.name}'
        and '{order.total}'.  Placeholders must match the keys in the
        mapping supplied to ``str.format``.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If *order_id* is invalid or if the template attempts to access
        restricted data (e.g., a customer SSN).
    """
    # Retrieve order and customer objects
    order = _get_order(order_id)
    customer = _get_customer(order.customer_id)

    # Build a context dictionary
    context: Dict[str, Any] = {
        "order.id": order.id,
        "order.total": f"${order.total:,.2f}",
        "order.items": ", ".join(order.items),
        "customer.id": customer.id,
        "customer.name": customer.name,
        "customer.email": customer.email,
    }

    # Add all non‑sensitive attributes of the customer
    for key, value in _sanitize_dict(customer.__dict__).items():
        context[f"customer.{key}"] = value

    # Security check: disallow placeholders that would expose sensitive data
    placeholder_pattern = re.compile(r"{([^}]+)}")
    for placeholder in placeholder_pattern.findall(template):
        if placeholder not in context:
            # If the placeholder refers to a sensitive field, raise an error
            if "ssn" in placeholder.lower():
                raise RestrictedAccessError(
                    f"Attempt to access restricted data: '{placeholder}'"
                )
            raise ValueError(f"Unknown placeholder in template: '{placeholder}'")

    try:
        receipt = template.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return receipt