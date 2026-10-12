import re
from typing import Any, Dict

# ------------------------------------------------------------------
# Simple in‑memory data store – replace with real database access
# ------------------------------------------------------------------

class Customer:
    """Represents a customer. Only public attributes are exposed."""
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class Order:
    """Represents an order. Holds a reference to the customer."""
    def __init__(self, id: str, total: float, items: Dict[str, int], customer: Customer):
        self.id = id
        self.total = total
        self.items = items          # e.g. {"apple": 2, "banana": 3}
        self.customer = customer

# Sample data – in a real system this would come from a DB
CUSTOMERS = {
    "cust1": Customer("Alice Smith", "alice@example.com"),
}
ORDERS = {
    "order123": Order(
        id="order123",
        total=59.99,
        items={"laptop": 1, "mouse": 2},
        customer=CUSTOMERS["cust1"],
    ),
}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def _safe_getattr(obj: Any, attr_path: str) -> Any:
    """
    Retrieve a nested attribute value following the dot notation in attr_path.
    Raises ValueError if any part of the path is a protected attribute
    (starts with an underscore).
    """
    parts = attr_path.split(".")
    current_obj: Any = obj
    for part in parts:
        if part.startswith("_"):
            raise ValueError(f"Access to protected attribute '{part}' is forbidden")
        if not hasattr(current_obj, part):
            raise ValueError(f"Attribute '{part}' not found in object of type {type(current_obj).__name__}")
        current_obj = getattr(current_obj, part)
    return current_obj

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def create_purchase_receipt(order_id: str, receipt_template: str) -> str:
    """
    Generate a receipt string by replacing placeholders in the template
    with values from the order and its customer.

    Placeholders are of the form {customer.name}, {order.total},
    {order.items.laptop} etc.

    Raises:
        ValueError: If the order_id is invalid or if a placeholder
                    references a protected attribute.
    """
    # Retrieve the order; raise error if not found
    order = ORDERS.get(order_id)
    if order is None:
        raise ValueError(f"Invalid order ID: {order_id}")

    # Build a context dictionary that maps top-level names to objects
    context = {
        "order": order,
        "customer": order.customer,
    }

    # Regex to find placeholders like {customer.name}
    placeholder_pattern = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

    def replace_placeholder(match: re.Match) -> str:
        expr = match.group(1)
        # Resolve the expression against the context
        try:
            parts = expr.split(".", 1)
            base_name, rest = parts[0], ".".join(parts[1:]) if len(parts) > 1 else ""
            base_obj = context.get(base_name)
            if base_obj is None:
                raise ValueError(f"Unknown placeholder '{expr}'")
            value = _safe_getattr(base_obj, rest) if rest else base_obj
        except ValueError as e:
            raise ValueError(f"Error processing placeholder '{{{expr}}}': {e}") from None
        # Convert value to string for replacement
        return str(value)

    # Perform substitution
    try:
        receipt = placeholder_pattern.sub(replace_placeholder, receipt_template)
    except ValueError as e:
        # Re‑raise with a clearer message
        raise ValueError(f"Failed to generate receipt: {e}") from None

    return receipt

# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Thank you for your purchase, {customer.name}!\n"
        "Order ID: {order.id}\n"
        "Total: ${order.total}\n"
        "Items:\n"
        "- Laptop x{order.items.laptop}\n"
        "- Mouse x{order.items.mouse}\n"
    )
    print(create_purchase_receipt("order123", template))