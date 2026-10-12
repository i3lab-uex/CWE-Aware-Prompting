import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Mock data layer (replace with real database access in production)
# ----------------------------------------------------------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str          # Sensitive
    address: str        # Sensitive

@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: list

# In‑memory “database”
CUSTOMERS: Dict[str, Customer] = {
    "c001": Customer(id="c001", name="Alice Smith",
                     email="alice@example.com", address="123 Main St"),
    "c002": Customer(id="c002", name="Bob Jones",
                     email="bob@example.com", address="456 Oak Ave"),
}

ORDERS: Dict[str, Order] = {
    "o100": Order(id="o100", customer_id="c001",
                  total=59.99, items=["Book", "Pen"]),
    "o101": Order(id="o101", customer_id="c002",
                  total=23.50, items=["Notebook"]),
}

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def generate_buyer_receipt(order_id: str, template: str) -> str:
    """
    Generates a buyer receipt by filling the provided template with order
    and customer data.

    Args:
        order_id: The unique identifier of the order.
        template: A string containing placeholders such as
                  '{customer.name}', '{order.total}'.

    Returns:
        The formatted receipt string.

    Raises:
        ValueError: If the order_id is unknown, if the customer data is
                    restricted, or if the template contains disallowed
                    placeholders.
    """
    # ------------------------------------------------------------------
    # 1. Validate order existence
    # ------------------------------------------------------------------
    order = ORDERS.get(order_id)
    if not order:
        raise ValueError(f"Order ID '{order_id}' does not exist.")

    # ------------------------------------------------------------------
    # 2. Retrieve associated customer
    # ------------------------------------------------------------------
    customer = CUSTOMERS.get(order.customer_id)
    if not customer:
        raise ValueError(f"Customer for order '{order_id}' is missing.")

    # ------------------------------------------------------------------
    # 3. Define whitelist of safe placeholders
    # ------------------------------------------------------------------
    allowed_placeholders = {
        "order.id",
        "order.total",
        "customer.name",
    }

    # ------------------------------------------------------------------
    # 4. Parse placeholders in template
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    placeholders_in_template = set(placeholder_pattern.findall(template))

    # Validate each placeholder
    for ph in placeholders_in_template:
        if ph not in allowed_placeholders:
            raise ValueError(f"Disallowed placeholder '{ph}' in template.")

    # ------------------------------------------------------------------
    # 5. Prepare substitution mapping
    # ------------------------------------------------------------------
    substitutions = {
        "order.id": order.id,
        "order.total": f"${order.total:,.2f}",
        "customer.name": customer.name,
    }

    # ------------------------------------------------------------------
    # 6. Perform substitution
    # ------------------------------------------------------------------
    def replacer(match):
        key = match.group(1)
        return substitutions[key]

    receipt = placeholder_pattern.sub(replacer, template)

    return receipt

# ----------------------------------------------------------------------
# Example usage (for testing purposes only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name}\n"
        "Total Amount: {order.total}"
    )
    print(generate_buyer_receipt("o100", tmpl))