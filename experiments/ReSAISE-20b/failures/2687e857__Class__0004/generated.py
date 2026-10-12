import re
from dataclasses import dataclass, field
from typing import Dict, Any

# ----------------------------------------------------------------------
# Sample data models (would normally come from the e‑commerce system)
# ----------------------------------------------------------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str  # public info, but could be considered sensitive in some contexts
    _ssn: str   # protected attribute – should not be exposed

@dataclass
class Order:
    id: str
    customer: Customer
    total: float
    items: list[Dict[str, Any]] = field(default_factory=list)

# ----------------------------------------------------------------------
# In‑memory "database" of orders for demo purposes
# ----------------------------------------------------------------------
ORDERS_DB: Dict[str, Order] = {}

def _populate_demo_data() -> None:
    """Populate ORDERS_DB with a couple of demo orders."""
    global ORDERS_DB
    cust1 = Customer(id="c001", name="Alice Smith", email="alice@example.com", _ssn="123-45-6789")
    cust2 = Customer(id="c002", name="Bob Jones", email="bob@example.com", _ssn="987-65-4321")

    ORDERS_DB["o100"] = Order(
        id="o100",
        customer=cust1,
        total=59.99,
        items=[{"name": "Widget", "qty": 2, "price": 19.99},
               {"name": "Gadget", "qty": 1, "price": 19.99}]
    )
    ORDERS_DB["o101"] = Order(
        id="o101",
        customer=cust2,
        total=89.95,
        items=[{"name": "Thingamajig", "qty": 3, "price": 29.98}]
    )

# Populate demo data on import
_populate_demo_data()

# ----------------------------------------------------------------------
# Utility helpers
# ----------------------------------------------------------------------
_placeholder_re = re.compile(r"\{([^\{\}]+)\}")

def _get_attr_safe(obj: Any, attr_name: str) -> Any:
    """
    Retrieve an attribute from obj safely.
    Raises ValueError if the attribute is protected (starts with '_').
    """
    if attr_name.startswith("_"):
        raise ValueError(f"Access to protected attribute '{attr_name}' is forbidden.")
    if not hasattr(obj, attr_name):
        raise ValueError(f"Attribute '{attr_name}' does not exist on object of type {type(obj).__name__}.")
    return getattr(obj, attr_name)

def _resolve_placeholder(match: re.Match, context: Dict[str, Any]) -> str:
    """
    Resolve a single placeholder using the provided context.
    """
    path = match.group(1).strip()
    # Split by '.' to support nested attributes (e.g., customer.name)
    parts = path.split(".")
    current_obj: Any = context
    for part in parts:
        if isinstance(current_obj, dict):
            if part not in current_obj:
                raise ValueError(f"Missing key '{part}' in context dictionary.")
            current_obj = current_obj[part]
        else:
            current_obj = _get_attr_safe(current_obj, part)
    # Convert the final value to string
    return str(current_obj)

# ----------------------------------------------------------------------
# Main function as required by the specification
# ----------------------------------------------------------------------
def create_transaction_receipt(transaction_id: str, temp_format: str) -> str:
    """
    Generate a receipt string for the given transaction_id using the provided template.

    Args:
        transaction_id: Identifier of the order.
        temp_format: Template string containing placeholders like '{customer.name}'.

    Returns:
        A formatted receipt string with all placeholders replaced by actual data.

    Raises:
        ValueError: If the transaction_id is invalid, or if a placeholder tries to
                    access protected customer information.
    """
    # 1. Retrieve the order
    if transaction_id not in ORDERS_DB:
        raise ValueError(f"Invalid transaction ID: {transaction_id}")

    order = ORDERS_DB[transaction_id]

    # 2. Build context dictionary for placeholder resolution
    context = {
        "order": order,
        "customer": order.customer,
    }

    # 3. Replace placeholders safely
    try:
        receipt = _placeholder_re.sub(lambda m: _resolve_placeholder(m, context), temp_format)
    except ValueError as e:
        # Re‑raise to match the specification
        raise

    return receipt


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total:.2f}\n"
        "Items:\n"
        "{items}"
    )

    # For items, we need a custom placeholder resolver
    def _custom_resolver(match: re.Match) -> str:
        if match.group(1).strip() == "items":
            items = ORDERS_DB["o100"].items
            return "\n".join(f"  - {i['name']} x{i['qty']} @ ${i['price']:.2f}" for i in items)
        raise ValueError("Unknown placeholder")

    # Replace {items} manually
    temp = template.replace("{items}", "")
    receipt = create_transaction_receipt("o100", temp)
    print(receipt)