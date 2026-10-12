import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Simple in‑memory data store for demonstration purposes.
# In a real system these would be fetched from a database or service.
# ----------------------------------------------------------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str
    phone: str
    # Sensitive fields that must never be exposed via the receipt template
    credit_card_number: str = field(repr=False, default='')
    ssn: str = field(repr=False, default='')

@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: Dict[str, int]  # item name -> quantity
    shipping_address: str

# Mock data store
CUSTOMERS = {
    "cust123": Customer(
        id="cust123",
        name="Alice Smith",
        email="alice@example.com",
        phone="+1-555-0123",
        credit_card_number="4111111111111111",
        ssn="123-45-6789"
    )
}

ORDERS = {
    "order456": Order(
        id="order456",
        customer_id="cust123",
        total=149.99,
        items={"Widget": 2, "Gadget": 1},
        shipping_address="123 Main St, Anytown, USA"
    )
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def get_order_by_id(order_id: str) -> Order:
    """Retrieve an order by its ID."""
    try:
        return ORDERS[order_id]
    except KeyError as exc:
        raise ValueError(f"Order with ID '{order_id}' not found") from exc

def get_customer_by_id(customer_id: str) -> Customer:
    """Retrieve a customer by its ID."""
    try:
        return CUSTOMERS[customer_id]
    except KeyError as exc:
        raise ValueError(f"Customer with ID '{customer_id}' not found") from exc

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
PLACEHOLDER_REGEX = re.compile(r"\{([a-zA-Z_][\w\.]*)\}")

# List of disallowed attribute names (case‑insensitive)
DISALLOWED_KEYS = {
    "credit_card_number",
    "ssn",
    "password",  # just in case
}

def generate_customer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order using the provided template.
    
    Parameters
    ----------
    order_id : str
        The ID of the order to generate a receipt for.
    template : str
        A string containing placeholders such as `{order.total}` or `{customer.name}`.
    
    Returns
    -------
    str
        The rendered receipt string with all placeholders replaced by actual data.
    
    Raises
    ------
    ValueError
        If the order or customer cannot be found, a placeholder refers to a disallowed key,
        or any other error occurs during rendering.
    """
    # Fetch order and customer data
    order = get_order_by_id(order_id)
    customer = get_customer_by_id(order.customer_id)

    # Helper to resolve a single placeholder
    def resolve_placeholder(match: re.Match) -> str:
        key_path = match.group(1).strip()
        
        # Disallow any reference to sensitive attributes
        for disallowed in DISALLOWED_KEYS:
            if disallowed.lower() in key_path.lower():
                raise ValueError(f"Access to sensitive field '{disallowed}' is prohibited")
        
        # Resolve nested attributes like 'order.total' or 'customer.name'
        parts = key_path.split(".")
        if not parts:
            raise ValueError(f"Invalid placeholder syntax: {match.group(0)}")
        
        # Determine the base object
        if parts[0] == "order":
            obj = order
        elif parts[0] == "customer":
            obj = customer
        else:
            raise ValueError(f"Unknown placeholder base '{parts[0]}' in {match.group(0)}")
        
        # Traverse the attributes
        for attr in parts[1:]:
            try:
                obj = getattr(obj, attr)
            except AttributeError as exc:
                raise ValueError(f"Attribute '{attr}' not found in {parts[0]}") from exc
        
        # Convert the final value to string
        return str(obj)

    try:
        receipt = PLACEHOLDER_REGEX.sub(resolve_placeholder, template)
    except Exception as exc:
        raise ValueError(f"Failed to render receipt: {exc}") from exc

    return receipt


# ----------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Items:\n"
    )
    for item, qty in ORDERS["order456"].items.items():
        tmpl += f"  - {item} x{qty}\n"
    tmpl += (
        "Total: ${order.total:.2f}\n"
        "Shipping to: {order.shipping_address}"
    )
    
    print(generate_customer_receipt("order456", tmpl))