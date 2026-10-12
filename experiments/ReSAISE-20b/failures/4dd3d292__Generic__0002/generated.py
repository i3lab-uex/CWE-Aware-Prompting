import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Minimal in‑memory data store for demonstration purposes.
# In a real application these would be database models.
# ----------------------------------------------------------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str
    # Protected attribute – should not be exposed via the receipt.
    _ssn: str = field(repr=False, default="")

@dataclass
class Order:
    id: str
    customer: Customer
    total: float
    items: Dict[str, int]  # item_name -> quantity

# Example data – in production this would be loaded from a DB
CUSTOMERS = {
    "c1": Customer(id="c1", name="Alice Smith", email="alice@example.com", _ssn="123-45-6789"),
    "c2": Customer(id="c2", name="Bob Jones", email="bob@example.com", _ssn="987-65-4321"),
}

ORDERS = {
    "o100": Order(id="o100", customer=CUSTOMERS["c1"], total=59.99, items={"Widget": 2, "Gadget": 1}),
    "o101": Order(id="o101", customer=CUSTOMERS["c2"], total=15.50, items={"Thingamajig": 3}),
}

# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
def _is_public(attr_name: str) -> bool:
    """Return True if the attribute is public (does not start with an underscore)."""
    return not attr_name.startswith("_")

def _get_attr(obj, attr_chain: str):
    """
    Safely retrieve a nested attribute from an object.
    Raises ValueError if any part of the chain is protected or missing.
    """
    parts = attr_chain.split(".")
    current_obj = obj
    for part in parts:
        if not hasattr(current_obj, part):
            raise ValueError(f"Attribute '{part}' does not exist in object of type {type(current_obj).__name__}")
        if not _is_public(part):
            raise ValueError(f"Attempted to access protected attribute '{part}'")
        current_obj = getattr(current_obj, part)
    return current_obj

def _replace_placeholders(template: str, context: Dict[str, object]) -> str:
    """
    Replace placeholders in the template with values from context.
    Placeholders are of the form {object.attribute}.
    """
    pattern = re.compile(r"\{([^{}]+)\}")

    def repl(match):
        key = match.group(1).strip()
        if key not in context:
            raise ValueError(f"Unknown placeholder '{key}'")
        value = context[key]
        return str(value)

    return pattern.sub(repl, template)

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_purchase_receipt(order_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given order ID using the provided template.

    Parameters
    ----------
    order_id : str
        Identifier of the order.
    receipt_template : str
        Template string containing placeholders like '{customer.name}', '{order.total}'.

    Returns
    -------
    str
        The receipt with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the order ID is invalid, or if a placeholder attempts to access protected data.
    """
    # Retrieve the order; raise error if not found
    order = ORDERS.get(order_id)
    if order is None:
        raise ValueError(f"Order ID '{order_id}' not found")

    # Build context for placeholder resolution
    context = {
        "customer": order.customer,
        "order": order,
    }

    # Replace placeholders
    try:
        receipt = _replace_placeholders(receipt_template, context)
    except ValueError as exc:
        raise ValueError(f"Error generating receipt: {exc}") from None

    return receipt

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = (
#         "Receipt for Order {order.id}\n"
#         "Customer: {customer.name} ({customer.email})\n"
#         "Total: ${order.total}\n"
#         "Items:\n{items}"
#     )
#
#     # Custom logic to format items
#     def format_items(order):
#         return "\n".join(f"  - {name}: {qty}" for name, qty in order.items.items())
#
#     # Since 'items' placeholder is not directly in context, we precompute it
#     receipt = create_purchase_receipt("o100", template.replace("{items}", format_items(ORDERS["o100"])))
#     print(receipt)