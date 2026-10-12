import re
from dataclasses import dataclass, field
from typing import Dict

# -------------------- Mock database and models --------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str
    # Sensitive field that must not be exposed via receipt
    ssn: str = field(repr=False)

@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: list

# In‑memory store for demonstration purposes
CUSTOMERS_DB: Dict[str, Customer] = {
    "c1": Customer(id="c1", name="Alice Smith", email="alice@example.com", ssn="123-45-6789"),
    "c2": Customer(id="c2", name="Bob Jones", email="bob@example.com", ssn="987-65-4321"),
}

ORDERS_DB: Dict[str, Order] = {
    "o100": Order(id="o100", customer_id="c1", total=49.99, items=["Book", "Pen"]),
    "o101": Order(id="o101", customer_id="c2", total=19.95, items=["Notebook"]),
}

# -------------------- Receipt generation logic --------------------
PLACEHOLDER_PATTERN = re.compile(r"\{([a-zA-Z_][\w\.]*)\}")

# Allowed placeholders mapped to their resolution functions
ALLOWED_PLACEHOLDERS = {
    "customer.name": lambda c, o: c.name,
    "customer.email": lambda c, o: c.email,
    "order.id":     lambda c, o: o.id,
    "order.total":  lambda c, o: f"{o.total:.2f}",
    "order.items":  lambda c, o: ", ".join(o.items),
}

def create_order_receipt(purchase_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given order ID using the supplied template.

    Parameters
    ----------
    purchase_id : str
        Unique identifier of the order.
    receipt_template : str
        Template string containing placeholders like '{customer.name}'.

    Returns
    -------
    str
        The receipt with all placeholders substituted.

    Raises
    ------
    ValueError
        If the order does not exist or a placeholder references restricted data.
    """
    # Retrieve the order
    order = ORDERS_DB.get(purchase_id)
    if not order:
        raise ValueError(f"Order ID '{purchase_id}' does not exist.")

    # Retrieve the customer
    customer = CUSTOMERS_DB.get(order.customer_id)
    if not customer:
        raise ValueError(f"Customer ID '{order.customer_id}' does not exist for order '{purchase_id}'.")

    # Find all placeholders in the template
    matches = PLACEHOLDER_PATTERN.findall(receipt_template)

    # Resolve each placeholder safely
    resolved_values = {}
    for key in set(matches):  # deduplicate to avoid repeated lookups
        if key not in ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Placeholder '{key}' is not allowed or does not exist.")
        try:
            resolved_values[key] = ALLOWED_PLACEHOLDERS[key](customer, order)
        except Exception as exc:
            raise ValueError(f"Failed to resolve placeholder '{key}': {exc}") from exc

    # Perform the substitution
    def replacement(match):
        placeholder = match.group(1)
        return str(resolved_values.get(placeholder, match.group(0)))

    receipt = PLACEHOLDER_PATTERN.sub(replacement, receipt_template)
    return receipt

# -------------------- Example usage (commented out) --------------------
# if __name__ == "__main__":
#     template = (
#         "Receipt for Order {order.id}\n"
#         "Customer: {customer.name} ({customer.email})\n"
#         "Items: {order.items}\n"
#         "Total Due: ${order.total}"
#     )
#     print(create_order_receipt("o100", template))