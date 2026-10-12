import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
# Domain models (simplified for this example)
# ------------------------------------------------------------------

@dataclass
class Customer:
    id: str
    name: str
    email: str
    is_restricted: bool = False  # flag indicating whether sensitive data can be exposed


@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: list


# ------------------------------------------------------------------
# In‑memory repositories (would normally be backed by a database)
# ------------------------------------------------------------------

_CUSTOMERS: Dict[str, Customer] = {
    "cust-001": Customer(id="cust-001", name="Alice Smith", email="alice@example.com"),
    "cust-002": Customer(id="cust-002", name="Bob Jones", email="bob@example.com", is_restricted=True),
}

_ORDERS: Dict[str, Order] = {
    "ord-1001": Order(id="ord-1001", customer_id="cust-001", total=199.99, items=["Widget A", "Gadget B"]),
    "ord-1002": Order(id="ord-1002", customer_id="cust-002", total=49.50, items=["Widget C"]),
}


def get_customer(customer_id: str) -> Customer:
    try:
        return _CUSTOMERS[customer_id]
    except KeyError as exc:
        raise ValueError(f"Customer ID '{customer_id}' not found") from exc


def get_order(order_id: str) -> Order:
    try:
        return _ORDERS[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' not found") from exc


# ------------------------------------------------------------------
# Helper for safe formatting
# ------------------------------------------------------------------

class _SafeFormatDict(dict):
    """
    A dict subclass that raises a ValueError if a placeholder key is missing.
    This prevents accidental leaking of raw placeholders in the output.
    """
    def __missing__(self, key):
        raise ValueError(f"Missing value for placeholder '{key}'")


# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------

def generate_buyer_receipt(order_id: str, template: str) -> str:
    """
    Generates a buyer receipt by filling in placeholders from the provided template.

    Args:
        order_id (str): The unique identifier of the order.
        template (str): A string containing placeholders like '{customer.name}' and
                        '{order.total}'.

    Returns:
        str: The formatted receipt string.

    Raises:
        ValueError: If the order ID is invalid, if restricted customer data
                    would be exposed, or if a placeholder cannot be resolved.
    """
    # Fetch order and associated customer
    order = get_order(order_id)
    customer = get_customer(order.customer_id)

    # Security check: disallow access to restricted customers
    if customer.is_restricted:
        raise ValueError(f"Access to restricted customer data for '{customer.id}' is denied")

    # Build a flat mapping of placeholder names to values
    context = {
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "order.items": ", ".join(order.items),
        "customer.id": customer.id,
        "customer.name": customer.name,
        "customer.email": customer.email,
    }

    # Use a regex to find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")

    def replace_placeholder(match):
        key = match.group(1)
        try:
            return str(context[key])
        except KeyError as exc:
            raise ValueError(f"Unknown placeholder '{key}' in template") from exc

    # Perform the replacement safely
    receipt = placeholder_pattern.sub(replace_placeholder, template)
    return receipt


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------

# if __name__ == "__main__":
#     tmpl = (
#         "Receipt for Order {order.id}\n"
#         "Customer: {customer.name} ({customer.email})\n"
#         "Items: {order.items}\n"
#         "Total: ${order.total}"
#     )
#     print(generate_buyer_receipt("ord-1001", tmpl))