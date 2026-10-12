import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------
# Mock domain classes (would normally come from the application)
# --------------------------------------------------------------------

@dataclass
class Customer:
    id: str
    name: str
    email: str
    # Restricted data – should never be exposed via receipt templates
    ssn: str = field(repr=False, compare=False)

@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: Dict[str, int]  # item name -> quantity

# --------------------------------------------------------------------
# In‑memory repositories (simple stand‑in for a real data source)
# --------------------------------------------------------------------

CUSTOMERS = {
    "cust_001": Customer(id="cust_001", name="Alice Smith",
                         email="alice@example.com", ssn="123-45-6789"),
    "cust_002": Customer(id="cust_002", name="Bob Jones",
                         email="bob@example.com", ssn="987-65-4321"),
}

ORDERS = {
    "order_1001": Order(id="order_1001", customer_id="cust_001",
                        total=120.50, items={"Book": 1, "Pen": 3}),
    "order_1002": Order(id="order_1002", customer_id="cust_002",
                        total=75.00, items={"Notebook": 2}),
}

# --------------------------------------------------------------------
# Helper utilities
# --------------------------------------------------------------------

# Regex to find all placeholders of the form {something}
PLACEHOLDER_RE = re.compile(r"{([^{}]+)}")

# Whitelist of allowed customer attributes that can appear in the receipt
ALLOWED_CUSTOMER_ATTRS = {"name", "email"}

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def generate_client_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt for the given order using the supplied template.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        Template string containing placeholders such as {customer.name}.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid, or if a restricted customer attribute is requested.
    """

    # 1. Validate order ID format (simple alphanumeric + underscore check)
    if not re.fullmatch(r"[A-Za-z0-9_]+", order_id):
        raise ValueError(f"Invalid order ID format: {order_id}")

    # 2. Retrieve the Order; raise if not found
    order = ORDERS.get(order_id)
    if order is None:
        raise ValueError(f"Order ID '{order_id}' does not exist")

    # 3. Retrieve the Customer; raise if not found
    customer = CUSTOMERS.get(order.customer_id)
    if customer is None:
        raise ValueError(f"Customer ID '{order.customer_id}' does not exist")

    # 4. Build a context dictionary for formatting
    context: Dict[str, str] = {
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
    }

    # Add items summary
    items_summary = ", ".join(f"{name} x{qty}" for name, qty in order.items.items())
    context["order.items"] = items_summary

    # Add allowed customer attributes
    for attr in ALLOWED_CUSTOMER_ATTRS:
        context[f"customer.{attr}"] = getattr(customer, attr)

    # 5. Verify that the template does not reference restricted data
    for placeholder in PLACEHOLDER_RE.findall(template):
        if placeholder.startswith("customer."):
            attr = placeholder.split(".", 1)[1]
            if attr not in ALLOWED_CUSTOMER_ATTRS:
                raise ValueError(f"Attempt to access restricted customer data: {placeholder}")

    # 6. Perform formatting safely
    try:
        receipt = template.format(**context)
    except KeyError as exc:
        # Unresolved placeholder
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return receipt