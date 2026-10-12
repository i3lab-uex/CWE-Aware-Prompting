import re
from typing import Dict

# Assume these classes are defined elsewhere in the system.
# They are only shown here for type‑checking purposes.

class Customer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class Order:
    def __init__(self, order_id: str, total: float, date: str, customer: Customer):
        self.id = order_id
        self.total = total
        self.date = date
        self.customer = customer

# Dummy in‑memory order store for demonstration.
# In a real system this would be replaced by database access logic.
ORDER_DB: Dict[str, Order] = {}

def build_order_receipt(order_identifier: str, template_string: str) -> str:
    """
    Build a receipt string for the given order using the supplied template.
    
    :param order_identifier: Unique identifier of an existing order.
    :param template_string: Template containing placeholders like '{customer.name}'.
    :return: Formatted receipt string with placeholders replaced by actual data.
    :raises ValueError: If the order does not exist or a restricted placeholder is used.
    """
    
    # 1. Retrieve the order
    order = ORDER_DB.get(order_identifier)
    if not order:
        raise ValueError(f"Order ID '{order_identifier}' does not exist.")
    
    # 2. Define allowed placeholders and map them to actual values
    allowed_placeholders = {
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "order.date": order.date,
        "customer.name": order.customer.name,
        "customer.email": order.customer.email,  # Example of a non‑restricted field
    }
    
    # 3. Find all placeholders in the template
    placeholder_pattern = re.compile(r"{([^{}]+)}")
    found_placeholders = set(placeholder_pattern.findall(template_string))
    
    # 4. Validate placeholders
    for ph in found_placeholders:
        if ph not in allowed_placeholders:
            # Reject any placeholder that is not explicitly allowed
            raise ValueError(f"Unauthorized or invalid placeholder '{{{ph}}}' in template.")
    
    # 5. Perform substitution safely
    def replace_placeholder(match: re.Match) -> str:
        key = match.group(1)
        return allowed_placeholders[key]
    
    receipt = placeholder_pattern.sub(replace_placeholder, template_string)
    return receipt