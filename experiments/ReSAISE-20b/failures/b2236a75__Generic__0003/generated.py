import re
from dataclasses import dataclass, field
from typing import Any, Dict

# ----------------------------------------------------------------------
# Mocked data models (replace with real implementations in production)
# ----------------------------------------------------------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str
    address: str
    # Sensitive attributes – should never be exposed via templates
    ssn: str = field(repr=False, default="***-**-****")
    credit_card_number: str = field(repr=False, default="**** **** **** 1234")


@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: Dict[str, int]  # item_name -> quantity
    status: str

# ----------------------------------------------------------------------
# Fake data store (replace with real database access)
# ----------------------------------------------------------------------
CUSTOMERS = {
    "cust_001": Customer(
        id="cust_001",
        name="Alice Smith",
        email="alice@example.com",
        address="123 Maple St, Springfield",
    ),
    "cust_002": Customer(
        id="cust_002",
        name="Bob Johnson",
        email="bob@example.com",
        address="456 Oak Ave, Shelbyville",
    ),
}

ORDERS = {
    "order_1001": Order(
        id="order_1001",
        customer_id="cust_001",
        total=129.99,
        items={"Widget A": 2, "Gadget B": 1},
        status="completed",
    ),
    "order_1002": Order(
        id="order_1002",
        customer_id="cust_002",
        total=79.50,
        items={"Widget C": 1},
        status="completed",
    ),
}

def get_order_by_id(order_id: str) -> Order:
    try:
        return ORDERS[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' not found") from exc

def get_customer_by_id(customer_id: str) -> Customer:
    try:
        return CUSTOMERS[customer_id]
    except KeyError as exc:
        raise ValueError(f"Customer ID '{customer_id}' not found") from exc

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
SENSITIVE_ATTRS = {"ssn", "credit_card_number"}

def _get_attr_chain(obj: Any, chain: str) -> Any:
    """
    Resolve a dotted attribute chain (e.g., 'customer.name') on an object.
    Raises ValueError if any part of the chain is missing or sensitive.
    """
    parts = chain.split(".")
    current_obj = obj
    for part in parts:
        if not hasattr(current_obj, part):
            raise ValueError(f"Attribute '{part}' not found in {current_obj!r}")
        if part in SENSITIVE_ATTRS:
            raise ValueError(f"Access to sensitive attribute '{part}' is prohibited")
        current_obj = getattr(current_obj, part)
    return current_obj

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
PLACEHOLDER_PATTERN = re.compile(r"\{([^{}]+)\}")

def generate_customer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order ID based on the provided template.
    The template may contain placeholders in the form '{order.total}' or
    '{customer.name}'. Placeholders are replaced with the corresponding data.
    
    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A string containing placeholders to be substituted.
    
    Returns
    -------
    str
        The formatted receipt string with all placeholders replaced.
    
    Raises
    ------
    ValueError
        If the order or customer cannot be found, if a placeholder references
        an unknown attribute, or if access to sensitive information is attempted.
    """
    # Retrieve order and customer objects
    order = get_order_by_id(order_id)
    customer = get_customer_by_id(order.customer_id)

    # Context mapping for placeholder resolution
    context = {"order": order, "customer": customer}

    def _replace(match: re.Match) -> str:
        key = match.group(1).strip()
        if "." not in key:
            raise ValueError(f"Invalid placeholder '{match.group(0)}': missing dot notation")
        root, chain = key.split(".", 1)
        if root not in context:
            raise ValueError(f"Unknown context '{root}' in placeholder '{match.group(0)}'")
        try:
            value = _get_attr_chain(context[root], chain)
        except ValueError as exc:
            raise ValueError(f"Error resolving placeholder '{match.group(0)}': {exc}") from exc
        return str(value)

    try:
        receipt = PLACEHOLDER_PATTERN.sub(_replace, template)
    except re.error as exc:
        raise ValueError(f"Template regex error: {exc}") from exc

    return receipt