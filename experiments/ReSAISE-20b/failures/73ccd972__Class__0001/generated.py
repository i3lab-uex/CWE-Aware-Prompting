import re
from typing import Dict

# ----------------------------------------------------------------------
# Assumed external classes and data store (simplified for this example)
# ----------------------------------------------------------------------


class Customer:
    """
    Represents a customer. Only public attributes that are safe to expose
    should be listed in the allowed fields dictionary below.
    """

    def __init__(self, name: str, email: str, phone: str,
                 address: str, credit_card_number: str):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        # Credit card number is considered sensitive and should never be exposed.
        self.credit_card_number = credit_card_number


class Order:
    """
    Represents an order. Only public attributes that are safe to expose
    should be listed in the allowed fields dictionary below.
    """

    def __init__(self, order_id: str, customer: Customer,
                 total: float, items: list):
        self.id = order_id
        self.customer = customer
        self.total = total
        self.items = items  # list of item descriptions


# In a real application this would be replaced by database queries.
ORDERS_DB: Dict[str, Order] = {}


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------


def _safe_getattr(obj, attr):
    """
    Safely get an attribute from an object. Raises AttributeError if the
    attribute does not exist.
    """
    try:
        return getattr(obj, attr)
    except AttributeError as exc:
        raise AttributeError(f"Attribute '{attr}' not found on {obj}") from exc


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------


def create_order_receipt(purchase_id: str, receipt_template: str) -> str:
    """
    Generate a receipt by substituting placeholders in the template with
    order and customer data.

    Args:
        purchase_id: Unique identifier of the order.
        receipt_template: Template string containing placeholders like
                          '{customer.name}' or '{order.total}'.

    Returns:
        A fully formatted receipt string.

    Raises:
        ValueError: If the order ID is not found or if a placeholder
                    requests restricted data.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve the order
    # ------------------------------------------------------------------
    order = ORDERS_DB.get(purchase_id)
    if not order:
        raise ValueError(f"Order ID '{purchase_id}' does not exist.")

    # ------------------------------------------------------------------
    # 2. Define allowed placeholder mapping
    # ------------------------------------------------------------------
    # Allowed fields for customer and order.
    ALLOWED_CUSTOMER_FIELDS = {
        "name",
        "email",
        "phone",
        "address",
    }

    ALLOWED_ORDER_FIELDS = {
        "id",
        "total",
        # 'items' is allowed but will be represented as a stringified list
    }

    # Helper to resolve placeholder value
    def resolve_placeholder(match):
        full_key = match.group(1).strip()  # e.g., 'customer.name'
        parts = full_key.split(".")
        if len(parts) != 2:
            raise ValueError(f"Invalid placeholder format: '{full_key}'")

        obj_name, attr = parts
        if obj_name == "customer":
            if attr not in ALLOWED_CUSTOMER_FIELDS:
                raise ValueError(f"Access to restricted customer field '{attr}' is denied.")
            return str(_safe_getattr(order.customer, attr))
        elif obj_name == "order":
            if attr not in ALLOWED_ORDER_FIELDS:
                raise ValueError(f"Access to restricted order field '{attr}' is denied.")
            return str(_safe_getattr(order, attr))
        else:
            raise ValueError(f"Unknown placeholder object '{obj_name}'.")

    # ------------------------------------------------------------------
    # 3. Perform substitution
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    try:
        formatted_receipt = placeholder_pattern.sub(resolve_placeholder, receipt_template)
    except ValueError as exc:
        # Re-raise with context
        raise ValueError(f"Failed to create receipt: {exc}") from exc

    return formatted_receipt


# ----------------------------------------------------------------------
# Example usage (for testing purposes only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Create sample data
    cust = Customer(
        name="Alice Smith",
        email="alice@example.com",
        phone="+1234567890",
        address="42 Wonderland Ave",
        credit_card_number="4111111111111111"
    )
    order = Order(
        order_id="ORD123",
        customer=cust,
        total=99.95,
        items=["Widget A", "Widget B"]
    )
    ORDERS_DB[order.id] = order

    template = (
        "Order Receipt\n"
        "-------------\n"
        "Order ID: {order.id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Phone: {customer.phone}\n"
        "Address: {customer.address}\n"
        "Total: ${order.total:.2f}\n"
    )

    print(create_order_receipt("ORD123", template))