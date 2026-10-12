import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict

# ----------------------------------------------------------------------
# Mock database and domain objects (replace with real implementations)
# ----------------------------------------------------------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str
    # Protected data that should never be exposed via the template
    ssn: str = field(repr=False, default="")

@dataclass
class Order:
    id: str
    customer: Customer
    total: float
    date: datetime

# In‑memory "database" of orders for demo purposes.
ORDER_DB: Dict[str, Order] = {}

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
ALLOWED_ORDER_FIELDS = {"id", "total", "date"}
ALLOWED_CUSTOMER_FIELDS = {"name", "email"}

def _resolve_path(root_obj, path: str):
    """
    Resolve a dotted attribute path on an object.
    Raises AttributeError if any part of the path is missing.
    """
    parts = path.split(".")
    obj = root_obj
    for part in parts:
        if not hasattr(obj, part):
            raise AttributeError(f"Attribute '{part}' not found on {obj!r}")
        obj = getattr(obj, part)
    return obj

def _format_value(value):
    """
    Convert values to string representation suitable for the receipt.
    Dates are formatted as ISO strings, floats are rounded to two decimals.
    """
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M")
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_order_receipt(order_identifier: str, template_string: str) -> str:
    """
    Generate a receipt string for the given order using the supplied template.

    Parameters
    ----------
    order_identifier : str
        Unique identifier of the order.
    template_string : str
        Template containing placeholders like '{customer.name}' or '{order.total}'.

    Returns
    -------
    str
        Formatted receipt with all placeholders replaced.

    Raises
    ------
    ValueError
        If the order ID does not exist or a placeholder requests restricted data.
    """
    # 1. Retrieve the order
    order = ORDER_DB.get(order_identifier)
    if not order:
        raise ValueError(f"Order with id '{order_identifier}' does not exist.")

    # 2. Prepare context objects
    context = {
        "order": order,
        "customer": order.customer,
    }

    # 3. Find all placeholders
    placeholder_pattern = re.compile(r"\{([^\{\}]+)\}")

    def replace_placeholder(match):
        placeholder = match.group(1).strip()
        # Validate and resolve the placeholder
        try:
            if placeholder.startswith("customer."):
                field_name = placeholder.split(".", 1)[1]
                if field_name not in ALLOWED_CUSTOMER_FIELDS:
                    raise ValueError(f"Access to restricted customer data '{field_name}'.")
                value = _resolve_path(context["customer"], field_name)
            elif placeholder.startswith("order."):
                field_name = placeholder.split(".", 1)[1]
                if field_name not in ALLOWED_ORDER_FIELDS:
                    raise ValueError(f"Access to restricted order data '{field_name}'.")
                value = _resolve_path(context["order"], field_name)
            else:
                raise ValueError(f"Unknown placeholder '{placeholder}'.")
        except AttributeError as e:
            raise ValueError(f"Invalid placeholder '{placeholder}': {e}")

        return _format_value(value)

    # 4. Substitute all placeholders
    receipt = placeholder_pattern.sub(replace_placeholder, template_string)
    return receipt

# ----------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Populate the mock database
    cust = Customer(id="C001", name="Alice Smith", email="alice@example.com", ssn="123-45-6789")
    order = Order(id="O1001", customer=cust, total=150.75, date=datetime.now())
    ORDER_DB[order.id] = order

    tmpl = (
        "Receipt for Order {order.id}\n"
        "Date: {order.date}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total Amount: ${order.total}\n"
    )

    print(build_order_receipt("O1001", tmpl))