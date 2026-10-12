import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------
# Data models
# ----------------------------

@dataclass
class Customer:
    """Represents a customer. Sensitive data is protected by prefixing with '_'."""
    id: str
    name: str
    email: str
    _credit_card_number: str = field(repr=False, default="")  # protected

@dataclass
class Order:
    """Represents an order."""
    id: str
    customer_id: str
    total: float
    items: Dict[str, int]  # item_name -> quantity

# ----------------------------
# In‑memory “database”
# ----------------------------

CUSTOMERS: Dict[str, Customer] = {
    "cust001": Customer(id="cust001", name="Alice Smith", email="alice@example.com",
                        _credit_card_number="4111111111111111"),
    "cust002": Customer(id="cust002", name="Bob Jones", email="bob@example.com",
                        _credit_card_number="5555555555554444"),
}

ORDERS: Dict[str, Order] = {
    "order1001": Order(id="order1001", customer_id="cust001",
                       total=149.99, items={"Widget A": 2, "Gadget B": 1}),
    "order1002": Order(id="order1002", customer_id="cust002",
                       total=89.50, items={"Widget C": 1}),
}

# ----------------------------
# Helper functions
# ----------------------------

def _get_attr(obj, attr_name: str):
    """
    Safely retrieve an attribute from an object.
    Raises ValueError if the attribute is protected (starts with '_').
    """
    if attr_name.startswith("_"):
        raise ValueError(f"Access to protected attribute '{attr_name}' is forbidden.")
    return getattr(obj, attr_name)

def _resolve_placeholder(match: re.Match):
    """
    Resolve a single placeholder in the format {object.attribute}.
    Supports 'customer' and 'order' objects.
    """
    expr = match.group(1).strip()
    try:
        obj_name, attr_name = expr.split(".", 1)
    except ValueError:
        raise ValueError(f"Invalid placeholder syntax: '{{{expr}}}'")

    if obj_name == "customer":
        obj = _current_customer
    elif obj_name == "order":
        obj = _current_order
    else:
        raise ValueError(f"Unknown object '{obj_name}' in placeholder '{{{expr}}}'")

    return str(_get_attr(obj, attr_name))

# ----------------------------
# Main function
# ----------------------------

def create_transaction_receipt(transaction_id: str, temp_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the provided template.

    Parameters
    ----------
    transaction_id : str
        Identifier of the order.
    temp_format : str
        Template string containing placeholders such as '{customer.name}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid, if the customer cannot be found,
        or if a placeholder references protected information.
    """
    global _current_customer, _current_order  # used in the placeholder resolver

    if transaction_id not in ORDERS:
        raise ValueError(f"Invalid order ID: {transaction_id}")

    _current_order = ORDERS[transaction_id]
    customer_id = _current_order.customer_id
    if customer_id not in CUSTOMERS:
        raise ValueError(f"Customer ID {customer_id} not found for order {transaction_id}")

    _current_customer = CUSTOMERS[customer_id]

    # Use regex to find all placeholders of the form {object.attribute}
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    try:
        receipt = placeholder_pattern.sub(_resolve_placeholder, temp_format)
    except ValueError as e:
        raise ValueError(f"Error generating receipt: {e}")

    return receipt

# ----------------------------
# Example usage (uncomment to test)
# ----------------------------

# if __name__ == "__main__":
#     template = (
#         "Receipt for Order {order.id}\n"
#         "Customer: {customer.name} ({customer.email})\n"
#         "Items:\n"
#         "{order.items}\n"
#         "Total: ${order.total:.2f}"
#     )
#     print(create_transaction_receipt("order1001", template))