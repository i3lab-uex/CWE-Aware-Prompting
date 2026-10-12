import re
from typing import Dict

# --- Mock data structures -----------------------------------------

class Customer:
    """Represents a customer with limited publicly exposed attributes."""
    def __init__(self, name: str, email: str, phone: str):
        self.name = name          # public
        self.email = email        # public
        self.phone = phone        # public
        self._ssn = "000-00-0000"  # protected

class Order:
    """Represents an order tied to a customer."""
    def __init__(self, transaction_id: str, customer: Customer,
                 total: float, items: Dict[str, int]):
        self.transaction_id = transaction_id
        self.customer = customer  # public reference
        self.total = total        # public
        self.items = items        # public

# --- In‑memory store (simulating a persistent resource) ----------
ORDERS_DB: Dict[str, Order] = {}

def add_order(order: Order):
    """Adds an order to the in‑memory store."""
    ORDERS_DB[order.transaction_id] = order

# --- Core implementation -------------------------------------------

PLACEHOLDER_REGEX = re.compile(r"\{([^}]+)\}")

# Whitelist of attributes that are allowed to be accessed
ALLOWED_CUSTOMER_ATTRS = {"name", "email", "phone"}
ALLOWED_ORDER_ATTRS = {"transaction_id", "total", "items"}

def _resolve_placeholder(obj, attr_path: str):
    """
    Resolve a dotted attribute path on an object.
    Raises ValueError if the attribute is not allowed or does not exist.
    """
    parts = attr_path.split(".")
    current_obj = obj
    for i, part in enumerate(parts):
        # First segment could be 'customer' or the object itself
        if i == 0 and part in ("customer", "order"):
            # Skip explicit 'customer' or 'order' tokens
            continue

        # Determine if we are accessing a Customer or Order attribute
        is_customer = isinstance(current_obj, Customer)
        allowed_attrs = ALLOWED_CUSTOMER_ATTRS if is_customer else ALLOWED_ORDER_ATTRS

        if part not in allowed_attrs:
            raise ValueError(f"Access to restricted attribute '{part}' is prohibited.")

        if not hasattr(current_obj, part):
            raise ValueError(f"Attribute '{part}' does not exist on {type(current_obj).__name__}.")

        current_obj = getattr(current_obj, part)

    return current_obj

def create_receipt_for_transaction(transaction_id: str, template_format: str) -> str:
    """
    Generate a receipt by substituting placeholders in the given template
    with actual customer and order data.

    Parameters:
        transaction_id (str): The unique ID of the order.
        template_format (str): Template string containing placeholders.

    Returns:
        str: The formatted receipt.

    Raises:
        ValueError: If the transaction ID is unknown or a placeholder
                    references restricted data.
    """
    # --- Retrieve order (resource acquisition) ----------------------
    order = ORDERS_DB.get(transaction_id)
    if not order:
        raise ValueError(f"Order with ID '{transaction_id}' does not exist.")

    # --- Replace placeholders --------------------------------------
    def replacement(match):
        placeholder = match.group(1).strip()
        # Allow either direct access or via 'customer'/'order'
        if placeholder.startswith("customer."):
            attr_path = placeholder
        elif placeholder.startswith("order."):
            attr_path = placeholder
        else:
            # Implicitly refer to order if not prefixed
            attr_path = f"order.{placeholder}"

        value = _resolve_placeholder(order, attr_path)
        # For non-string values (e.g., dict), convert to string
        return str(value)

    receipt = PLACEHOLDER_REGEX.sub(replacement, template_format)
    return receipt

# --- Example usage -----------------------------------------------
if __name__ == "__main__":
    # Create sample data
    cust = Customer(name="Alice Smith", email="alice@example.com", phone="+123456789")
    order = Order(
        transaction_id="TXN1001",
        customer=cust,
        total=149.99,
        items={"widget": 2, "gadget": 1}
    )
    add_order(order)

    # Define a template
    tmpl = (
        "Receipt for Order {order.transaction_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total}\n"
        "Items: {order.items}"
    )

    # Generate receipt
    print(create_receipt_for_transaction("TXN1001", tmpl))