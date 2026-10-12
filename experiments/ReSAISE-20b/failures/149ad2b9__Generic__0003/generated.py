import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Dummy data models (replace with actual implementations in the real system)
# ----------------------------------------------------------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str
    phone: str
    # sensitive or restricted fields (e.g., credit card)
    _credit_card_number: str = field(repr=False, default="")

@dataclass
class Order:
    id: str
    customer: Customer
    items: list  # list of (product_name, quantity, unit_price)
    total: float

# ----------------------------------------------------------------------
# In-memory mock database (replace with real DB access in production)
# ----------------------------------------------------------------------
CUSTOMERS: Dict[str, Customer] = {
    "cust_1": Customer(id="cust_1", name="Alice Smith",
                       email="alice@example.com", phone="+1234567890"),
}
ORDERS: Dict[str, Order] = {
    "order_1": Order(id="order_1",
                     customer=CUSTOMERS["cust_1"],
                     items=[("Book", 2, 12.5), ("Pen", 5, 1.2)],
                     total=35.0),
}

# ----------------------------------------------------------------------
# Allowed placeholder mapping
# ----------------------------------------------------------------------
ALLOWED_PLACEHOLDERS = {
    "customer.id": lambda c: c.id,
    "customer.name": lambda c: c.name,
    "customer.email": lambda c: c.email,
    "customer.phone": lambda c: c.phone,
    "order.id": lambda o: o.id,
    "order.total": lambda o: f"{o.total:.2f}",
    # Add more mappings as needed
}

# ----------------------------------------------------------------------
# Helper to extract placeholders from template
# ----------------------------------------------------------------------
PLACEHOLDER_REGEX = re.compile(r"\{([^{}]+)\}")

def create_receipt_for_transaction(transaction_id: str, template_format: str) -> str:
    """
    Generate a receipt string for the given transaction id and template.

    Args:
        transaction_id: The unique identifier of an order.
        template_format: A string containing placeholders like `{customer.name}`.

    Returns:
        The fully formatted receipt string.

    Raises:
        ValueError: If the order does not exist or a restricted placeholder is used.
    """
    # Retrieve order
    order = ORDERS.get(transaction_id)
    if not order:
        raise ValueError(f"Order with id '{transaction_id}' does not exist.")

    customer = order.customer

    # Find all placeholders
    placeholders = set(PLACEHOLDER_REGEX.findall(template_format))

    # Validate placeholders and build replacement dict
    replacements = {}
    for key in placeholders:
        if key not in ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Unsupported placeholder '{key}'.")
        # Resolve value
        if key.startswith("customer."):
            value = ALLOWED_PLACEHOLDERS[key](customer)
        else:  # order.* placeholders
            value = ALLOWED_PLACEHOLDERS[key](order)
        replacements[key] = value

    # Perform safe substitution
    def replace_match(match: re.Match) -> str:
        key = match.group(1)
        return replacements[key]

    receipt = PLACEHOLDER_REGEX.sub(replace_match, template_format)

    return receipt

# ----------------------------------------------------------------------
# Example usage (commented out – remove for production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total}\n"
    )
    print(create_receipt_for_transaction("order_1", tmpl))