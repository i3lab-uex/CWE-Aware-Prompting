import re
from typing import Dict

# ------------------------------------------------------------------
# Mocked data structures (in a real system these would be ORM models)
# ------------------------------------------------------------------

class Customer:
    def __init__(self, name: str, email: str):
        self.name = name          # public
        self.email = email        # public
        self._ssn = "123-45-6789"  # protected (should not be exposed)

class Order:
    def __init__(self, order_id: str, customer: Customer, total: float):
        self.order_id = order_id  # public
        self.customer = customer  # public
        self.total = total          # public
        self._internal_code = "XYZ123"  # protected

# ------------------------------------------------------------------
# In‑memory "database"
# ------------------------------------------------------------------

ORDERS: Dict[str, Order] = {}
CUSTOMERS: Dict[str, Customer] = {}

# Populate with example data
cust1 = Customer("Alice Smith", "alice@example.com")
ORDERS["ORD001"] = Order("ORD001", cust1, 149.99)

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def _get_attr_chain(obj, chain: str):
    """
    Resolve a dotted attribute chain on an object.
    Raises ValueError if any attribute in the chain is protected (starts with '_').
    """
    parts = chain.split(".")
    current = obj
    for part in parts:
        if not hasattr(current, part):
            raise ValueError(f"Attribute '{part}' does not exist on {type(current).__name__}")
        if part.startswith("_"):
            raise ValueError(f"Attempt to access protected attribute '{part}'")
        current = getattr(current, part)
    return current

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")

def create_purchase_receipt(order_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt string for the given order ID using the supplied template.

    Parameters
    ----------
    order_id : str
        Identifier of the order.
    receipt_template : str
        Template string containing placeholders like '{customer.name}' or '{order.total}'.

    Returns
    -------
    str
        The formatted receipt string with placeholders replaced by actual values.

    Raises
    ------
    ValueError
        If the order ID is invalid, or if a placeholder refers to a protected attribute.
    """
    # Validate and retrieve the order
    order = ORDERS.get(order_id)
    if not order:
        raise ValueError(f"Order ID '{order_id}' is invalid or does not exist.")

    # Prepare context for placeholder resolution
    context = {"order": order, "customer": order.customer}

    def replace_placeholder(match: re.Match) -> str:
        key = match.group(1).strip()
        if not key:
            raise ValueError("Empty placeholder found in template.")
        # Resolve the value using the context
        if key not in context:
            raise ValueError(f"Unknown placeholder '{key}'.")
        value = _get_attr_chain(context[key], key.split(".", 1)[-1])
        return str(value)

    # Perform substitution
    try:
        receipt = PLACEHOLDER_RE.sub(replace_placeholder, receipt_template)
    except ValueError as exc:
        # Re‑raise to propagate error messages
        raise

    return receipt

# ------------------------------------------------------------------
# Example usage (commented out – for reference only)
# ------------------------------------------------------------------

# if __name__ == "__main__":
#     template = (
#         "Dear {customer.name},\n"
#         "Thank you for your purchase!\n"
#         "Order ID: {order.order_id}\n"
#         "Total: ${order.total:.2f}\n"
#     )
#     print(create_purchase_receipt("ORD001", template))