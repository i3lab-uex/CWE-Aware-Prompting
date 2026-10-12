import re
from typing import Dict, Any

# ------------------------------------------------------------------
# Assumed pre‑defined data structures (minimal mockup for illustration)
# ------------------------------------------------------------------

class Customer:
    def __init__(self, name: str, email: str, ssn: str):
        self.name = name
        self.email = email
        self.ssn = ssn          # Sensitive data – should never be exposed

class Order:
    def __init__(self, order_id: str, total: float, date: str, customer: Customer):
        self.id = order_id
        self.total = total
        self.date = date
        self.customer = customer

# Example in‑memory order store (would normally be a database)
ORDERS_DB: Dict[str, Order] = {}

# ------------------------------------------------------------------
# Receipt generation logic
# ------------------------------------------------------------------

# Allowed (public) fields that may appear in the template
ALLOWED_CUSTOMER_FIELDS = {"name", "email"}
ALLOWED_ORDER_FIELDS = {"id", "total", "date"}

# Regular expression to capture placeholders like {customer.name}
PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _get_placeholder_value(entity: Any, field_name: str) -> str:
    """
    Safely retrieve the value of a public attribute from an entity.
    Raises ValueError if the field is not allowed or does not exist.
    """
    # Check attribute existence
    if not hasattr(entity, field_name):
        raise ValueError(f"Field '{field_name}' does not exist on {entity.__class__.__name__}")
    # Retrieve value
    return str(getattr(entity, field_name))

def build_order_receipt(order_identifier: str, template_string: str) -> str:
    """
    Generate a receipt string by substituting placeholders in the template
    with data from the specified order and its customer.

    Raises:
        ValueError: If the order ID is invalid or a placeholder refers to
                    restricted data.
    """
    # Retrieve the order from the database
    order = ORDERS_DB.get(order_identifier)
    if not order:
        raise ValueError(f"Order ID '{order_identifier}' does not exist")

    # Function to replace each placeholder
    def _replace(match: re.Match) -> str:
        entity_name, field_name = match.group(1), match.group(2)

        # Validate entity and field
        if entity_name == "customer":
            if field_name not in ALLOWED_CUSTOMER_FIELDS:
                raise ValueError(f"Access to restricted customer field '{field_name}' is denied")
            return _get_placeholder_value(order.customer, field_name)

        if entity_name == "order":
            if field_name not in ALLOWED_ORDER_FIELDS:
                raise ValueError(f"Access to restricted order field '{field_name}' is denied")
            return _get_placeholder_value(order, field_name)

        raise ValueError(f"Unknown entity '{entity_name}' in placeholder")

    # Perform the substitution
    try:
        result = PLACEHOLDER_RE.sub(_replace, template_string)
    except ValueError as exc:
        # Re‑raise to signal caller
        raise

    return result

# ------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Populate mock database
    cust = Customer(name="Alice Smith", email="alice@example.com", ssn="123-45-6789")
    ORDERS_DB["ORD001"] = Order(order_id="ORD001", total=199.99, date="2023-08-15", customer=cust)

    template = (
        "Receipt for Order {order.id}\n"
        "Date: {order.date}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total}\n"
    )

    print(build_order_receipt("ORD001", template))