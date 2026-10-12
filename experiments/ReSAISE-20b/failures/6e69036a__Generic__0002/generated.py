import re
from dataclasses import dataclass
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Domain models (minimal implementation for this exercise)
# ----------------------------------------------------------------------


@dataclass
class Customer:
    """Represents a customer in the e‑commerce system."""
    id: str
    name: str
    email: str  # considered sensitive / restricted
    address: str


@dataclass
class Order:
    """Represents an order in the e‑commerce system."""
    id: str
    total: float
    customer: Customer


# ----------------------------------------------------------------------
# In‑memory repository (stand‑in for a real database or service)
# ----------------------------------------------------------------------


# Sample data
CUSTOMERS: Dict[str, Customer] = {
    "c001": Customer(id="c001", name="Alice Smith", email="alice@example.com",
                     address="123 Main St, Townsville"),
    "c002": Customer(id="c002", name="Bob Jones", email="bob@example.com",
                     address="456 Oak Ave, Villageton"),
}

ORDERS: Dict[str, Order] = {
    "o1001": Order(id="o1001", total=199.99, customer=CUSTOMERS["c001"]),
    "o1002": Order(id="o1002", total=49.95, customer=CUSTOMERS["c002"]),
}


def get_order_by_id(order_id: str) -> Optional[Order]:
    """Retrieve an Order by its ID, or None if not found."""
    return ORDERS.get(order_id)


# ----------------------------------------------------------------------
# Receipt generation logic
# ----------------------------------------------------------------------


RESTRICTED_FIELDS = {
    "customer.email",
}

PLACEHOLDER_REGEX = re.compile(r"\{([^\}]+)\}")


def generate_client_receipt(order_id: str, template: str) -> str:
    """
    Generate a formatted receipt for the given order ID using the supplied
    template.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A string containing placeholders such as `{customer.name}` or
        `{order.total}`.

    Returns
    -------
    str
        The receipt string with all placeholders substituted.

    Raises
    ------
    ValueError
        If the order ID is invalid, or if a restricted field is referenced in
        the template.
    """
    # 1. Validate order ID and retrieve data
    order = get_order_by_id(order_id)
    if not order:
        raise ValueError(f"Invalid order ID: {order_id}")

    # 2. Scan template for placeholders
    placeholders = PLACEHOLDER_REGEX.findall(template)

    for ph in placeholders:
        # e.g., 'customer.name', 'order.total'
        if ph in RESTRICTED_FIELDS:
            raise ValueError(f"Attempt to access restricted field '{ph}'")

        # Basic validation: ensure the placeholder refers to a known entity
        if ph.startswith("customer.") or ph.startswith("order."):
            continue  # acceptable
        else:
            raise ValueError(f"Unknown placeholder '{ph}' in template")

    # 3. Prepare context for formatting
    # The format() method can access attributes of the objects directly.
    context = {"customer": order.customer, "order": order}

    # 4. Perform formatting
    try:
        receipt = template.format(**context)
    except AttributeError as exc:
        # This typically means the placeholder refers to a missing attribute
        raise ValueError(f"Invalid placeholder in template: {exc}") from exc

    return receipt


# ----------------------------------------------------------------------
# Example usage (for manual testing only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name}\n"
        "Total: ${order.total:.2f}\n"
    )
    print(generate_client_receipt("o1001", tmpl))