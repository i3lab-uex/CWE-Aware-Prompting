import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------
# Mocked data models (in a real system these would come from the database)
# --------------------------------------------------------------------

@dataclass
class Customer:
    id: str
    name: str
    email: str
    # Sensitive field – should never be exposed unless explicitly permitted
    ssn: str

@dataclass
class Order:
    id: str
    total: float
    customer_id: str

# --------------------------------------------------------------------
# In‑memory registries (replace with real persistence in production)
# --------------------------------------------------------------------

CUSTOMERS: Dict[str, Customer] = {
    "c001": Customer(id="c001", name="Alice Smith", email="alice@example.com",
                     ssn="123-45-6789"),
    "c002": Customer(id="c002", name="Bob Jones", email="bob@example.com",
                     ssn="987-65-4321"),
}

ORDERS: Dict[str, Order] = {
    "o100": Order(id="o100", total=59.99, customer_id="c001"),
    "o101": Order(id="o101", total=120.00, customer_id="c002"),
}

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------

PLACEHOLDER_PATTERN = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

# Allowed placeholder names – anything not listed is considered restricted
ALLOWED_PLACEHOLDERS = {
    "order.id",
    "order.total",
    "customer.name",
    "customer.email",
}

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in PLACEHOLDER_PATTERN.finditer(template)}

def _build_context(order: Order, customer: Customer) -> dict:
    """Return a mapping of placeholder names to their values."""
    return {
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "customer.name": customer.name,
        "customer.email": customer.email,
    }

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def generate_client_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order using the provided template.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        Receipt pattern containing placeholders such as '{customer.name}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is unknown or if the template contains a restricted placeholder.
    """
    # Validate and fetch the order
    order = ORDERS.get(order_id)
    if not order:
        raise ValueError(f"Invalid order ID: {order_id}")

    # Validate and fetch the customer
    customer = CUSTOMERS.get(order.customer_id)
    if not customer:
        raise ValueError(f"Customer for order {order_id} not found")

    # Extract placeholders from the template
    placeholders = _extract_placeholders(template)

    # Check for restricted placeholders
    for ph in placeholders:
        if ph not in ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Attempt to expose restricted data via placeholder '{ph}'")

    # Build the context for formatting
    context = _build_context(order, customer)

    try:
        receipt = template.format(**context)
    except KeyError as exc:
        # This should not happen if placeholder validation passed
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return receipt

# --------------------------------------------------------------------
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total}\n"
    )
    print(generate_client_receipt("o100", tmpl))