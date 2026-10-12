import re
from dataclasses import dataclass, field
from typing import Dict

# -------------------------------------------------------------
# Dummy data structures (in a real system these would be ORM models)
# -------------------------------------------------------------

@dataclass
class Customer:
    id: str
    name: str
    email: str
    phone: str
    address: str
    # protected fields that must not be exposed in receipts
    _password: str = field(repr=False, default="secret")
    # any other sensitive fields can be added here

@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: Dict[str, int]  # item name -> quantity
    status: str

# In-memory "database" for demonstration purposes
CUSTOMERS = {
    "c001": Customer(id="c001", name="Alice Smith", email="alice@example.com",
                     phone="555-0100", address="123 Main St"),
    "c002": Customer(id="c002", name="Bob Jones", email="bob@example.com",
                     phone="555-0200", address="456 Oak Ave"),
}

ORDERS = {
    "o1001": Order(id="o1001", customer_id="c001", total=59.99,
                   items={"T-shirt": 2, "Mug": 1}, status="shipped"),
    "o1002": Order(id="o1002", customer_id="c002", total=120.50,
                   items={"Laptop": 1}, status="processing"),
}

# -------------------------------------------------------------
# Core function
# -------------------------------------------------------------

PLACEHOLDER_PATTERN = re.compile(r"\{([^}]+)\}")

def _get_attr(obj, attr_path: str):
    """
    Safely retrieve nested attributes separated by dots.
    Raises AttributeError if any part is missing or protected.
    """
    parts = attr_path.split(".")
    current = obj
    for part in parts:
        # Disallow access to attributes starting with underscore
        if part.startswith("_"):
            raise AttributeError(f"Access to protected attribute '{part}' is not allowed.")
        if hasattr(current, part):
            current = getattr(current, part)
        else:
            raise AttributeError(f"Attribute '{part}' not found in {type(current).__name__}.")
    return current

def create_order_receipt(purchase_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given order ID using the provided template.
    
    Parameters
    ----------
    purchase_id : str
        Unique identifier of the order.
    receipt_template : str
        Template string containing placeholders like `{customer.name}` or `{order.total}`.
    
    Returns
    -------
    str
        The receipt string with placeholders substituted by actual values.
    
    Raises
    ------
    ValueError
        If the order ID does not exist or a placeholder requests restricted data.
    """
    # 1. Validate existence of order
    order = ORDERS.get(purchase_id)
    if not order:
        raise ValueError(f"Order with ID '{purchase_id}' does not exist.")
    
    # 2. Retrieve associated customer
    customer = CUSTOMERS.get(order.customer_id)
    if not customer:
        raise ValueError(f"Customer with ID '{order.customer_id}' does not exist.")
    
    # 3. Prepare context for placeholder replacement
    context = {
        "order": order,
        "customer": customer,
    }
    
    # 4. Replace placeholders
    def replacer(match: re.Match):
        placeholder = match.group(1).strip()
        if "." not in placeholder:
            raise ValueError(f"Invalid placeholder '{placeholder}'. Expected format '{{object.attribute}}'.")
        obj_name, attr_path = placeholder.split(".", 1)
        if obj_name not in context:
            raise ValueError(f"Unknown placeholder object '{obj_name}'.")
        try:
            value = _get_attr(context[obj_name], attr_path)
        except AttributeError as exc:
            raise ValueError(str(exc)) from None
        return str(value)
    
    try:
        receipt = PLACEHOLDER_PATTERN.sub(replacer, receipt_template)
    except ValueError as exc:
        raise
    
    return receipt

# -------------------------------------------------------------
# Example usage (uncomment to test)
# -------------------------------------------------------------

# if __name__ == "__main__":
#     template = (
#         "Receipt for Order {order.id}\n"
#         "Customer: {customer.name} ({customer.email})\n"
#         "Total: ${order.total:.2f}\n"
#         "Status: {order.status}"
#     )
#     print(create_order_receipt("o1001", template))