import re
from typing import Dict

# ------------------------------------------------------------------
# Mocked domain classes (replace with real implementations)
# ------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str, address: str, phone: str):
        self.name = name
        self.email = email
        self.address = address
        self.phone = phone
        # Sensitive fields that must not be exposed
        self.ssn = "123-45-6789"
        self.credit_card_number = "4111111111111111"

class Order:
    def __init__(self, order_id: str, total: float, items: list, customer: Customer):
        self.order_id = order_id
        self.total = total
        self.items = items  # list of (item_name, qty, price)
        self.customer = customer

# ------------------------------------------------------------------
# In‑memory “database” of orders (replace with real data access)
# ------------------------------------------------------------------
ORDERS_DB: Dict[str, Order] = {}

def get_order_by_id(order_id: str) -> Order:
    """Retrieve an order from the database or raise ValueError."""
    if order_id not in ORDERS_DB:
        raise ValueError(f"Order ID '{order_id}' does not exist.")
    return ORDERS_DB[order_id]

# ------------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------------
_RE_PLACEHOLDER = re.compile(r"\{([^{}]+)\}")

def _safe_getattr(obj, attr):
    """Get attribute value if it exists; otherwise raise."""
    if not hasattr(obj, attr):
        raise ValueError(f"Attribute '{attr}' not found.")
    return getattr(obj, attr)

def _build_placeholder_map(order: Order) -> Dict[str, str]:
    """
    Build a mapping from placeholder keys to string values.
    Only expose non‑sensitive fields.
    """
    # Define allowed fields for customer and order
    allowed_customer_fields = {"name", "email", "address", "phone"}
    allowed_order_fields = {"order_id", "total"}

    # Customer data
    customer_map = {}
    for field in allowed_customer_fields:
        try:
            val = _safe_getattr(order.customer, field)
            customer_map[f"customer.{field}"] = str(val)
        except ValueError:
            # Should never happen because we only use allowed fields
            pass

    # Order data
    order_map = {}
    for field in allowed_order_fields:
        try:
            val = _safe_getattr(order, field)
            order_map[f"order.{field}"] = str(val)
        except ValueError:
            pass

    # Combine
    return {**customer_map, **order_map}

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_receipt_for_transaction(transaction_id: str, template_format: str) -> str:
    """
    Generate a receipt string by replacing placeholders in `template_format`
    with actual customer and order data.

    Parameters
    ----------
    transaction_id : str
        Unique identifier of the order.
    template_format : str
        Template containing placeholders like `{customer.name}`.

    Returns
    -------
    str
        Formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID does not exist or a placeholder requests restricted data.
    """
    # Retrieve the order
    order = get_order_by_id(transaction_id)

    # Build placeholder mapping
    placeholder_map = _build_placeholder_map(order)

    # Find all placeholders in the template
    placeholders_in_template = set(_RE_PLACEHOLDER.findall(template_format))

    # Validate that all placeholders are allowed
    for placeholder in placeholders_in_template:
        if placeholder not in placeholder_map:
            # Either the field is restricted or simply does not exist
            raise ValueError(f"Restricted or unknown placeholder '{placeholder}' in template.")

    # Perform substitution
    def replace(match):
        key = match.group(1)
        return placeholder_map[key]

    receipt = _RE_PLACEHOLDER.sub(replace, template_format)
    return receipt

# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     cust = Customer("Alice Smith", "alice@example.com", "123 Main St", "+1-555-0100")
#     order = Order("ORD12345", 99.95, [("Widget", 2, 19.99), ("Gadget", 1, 59.97)], cust)
#     ORDERS_DB[order.order_id] = order
#
#     template = (
#         "Receipt for Order {order.order_id}\n"
#         "Customer: {customer.name}\n"
#         "Email: {customer.email}\n"
#         "Total: ${order.total}\n"
#     )
#
#     print(create_receipt_for_transaction("ORD12345", template))