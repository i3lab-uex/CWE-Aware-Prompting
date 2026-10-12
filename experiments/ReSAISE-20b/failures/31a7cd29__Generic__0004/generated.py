import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------
# Mock data structures and store
# ------------------------------

@dataclass
class Customer:
    id: str
    name: str
    email: str
    address: str
    # Restricted data (not exposed via the receipt)
    ssn: str = field(repr=False, default="")
    password: str = field(repr=False, default="")

@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: Dict[str, int]  # item name -> quantity

# In‑memory "database"
CUSTOMERS: Dict[str, Customer] = {
    "c001": Customer(id="c001", name="Alice Smith",
                     email="alice@example.com",
                     address="123 Main St, Anytown",
                     ssn="123-45-6789", password="secret"),
    "c002": Customer(id="c002", name="Bob Jones",
                     email="bob@example.com",
                     address="456 Oak Ave, Othertown",
                     ssn="987-65-4321", password="topsecret"),
}

ORDERS: Dict[str, Order] = {
    "o100": Order(id="o100", customer_id="c001",
                  total=49.99, items={"Widget": 2, "Gadget": 1}),
    "o101": Order(id="o101", customer_id="c002",
                  total=79.50, items={"Thingamajig": 3}),
}

# ------------------------------
# Receipt builder
# ------------------------------

PLACEHOLDER_PATTERN = re.compile(r"\{([^}]+)\}")

# Allowed fields for each entity
ALLOWED_FIELDS = {
    "customer": {"name", "email", "address"},
    "order": {"id", "total", "items"},
}

# Helper functions to fetch data
def _get_order(order_id: str) -> Order:
    order = ORDERS.get(order_id)
    if not order:
        raise ValueError(f"Order ID '{order_id}' does not exist.")
    return order

def _get_customer(customer_id: str) -> Customer:
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        raise ValueError(f"Customer ID '{customer_id}' does not exist.")
    return customer

def build_order_receipt(order_identifier: str, template_string: str) -> str:
    """
    Build a receipt string for the given order by substituting placeholders
    with actual customer and order data.

    Raises:
        ValueError: If the order ID is invalid or if a restricted field is requested.
    """
    # Retrieve order and customer
    order = _get_order(order_identifier)
    customer = _get_customer(order.customer_id)

    # Prepare a mapping of placeholder -> value
    values: Dict[str, str] = {}

    for match in PLACEHOLDER_PATTERN.finditer(template_string):
        placeholder = match.group(1).strip()  # e.g., "customer.name"
        if "." not in placeholder:
            raise ValueError(f"Invalid placeholder format: '{{{placeholder}}}'")
        entity, field_name = placeholder.split(".", 1)

        if entity not in ALLOWED_FIELDS:
            raise ValueError(f"Unknown placeholder entity '{entity}'")

        if field_name not in ALLOWED_FIELDS[entity]:
            raise ValueError(f"Access to restricted field '{placeholder}' is not allowed")

        # Resolve the value
        if entity == "customer":
            value = getattr(customer, field_name)
        elif entity == "order":
            # Special handling for dicts/lists to avoid exposing raw objects
            attr = getattr(order, field_name)
            if isinstance(attr, dict):
                value = ", ".join(f"{k} x{v}" for k, v in attr.items())
            else:
                value = attr
        else:  # pragma: no cover
            raise ValueError(f"Unhandled entity '{entity}'")

        values[placeholder] = str(value)

    # Perform the substitution
    try:
        receipt = template_string.format(**values)
    except KeyError as exc:
        raise ValueError(f"Missing value for placeholder: {exc}") from exc

    return receipt