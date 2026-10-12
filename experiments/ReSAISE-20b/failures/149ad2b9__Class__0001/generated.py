import re
from dataclasses import dataclass
from typing import Dict, Any

# ------------------------------------------------------------------
# Mock data structures (in a real system these would come from a DB)
# ------------------------------------------------------------------

@dataclass
class Customer:
    id: str
    name: str
    email: str
    address: str
    phone: str
    # Sensitive fields (should never be exposed in a receipt)
    ssn: str = ""
    credit_card_number: str = ""

@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: list  # List of dicts with item details

# In-memory stores for demonstration purposes
CUSTOMERS: Dict[str, Customer] = {}
ORDERS: Dict[str, Order] = {}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def _get_customer(customer_id: str) -> Customer:
    """Retrieve a customer by ID or raise ValueError."""
    try:
        return CUSTOMERS[customer_id]
    except KeyError:
        raise ValueError(f"Customer with ID '{customer_id}' does not exist.")

def _get_order(order_id: str) -> Order:
    """Retrieve an order by ID or raise ValueError."""
    try:
        return ORDERS[order_id]
    except KeyError:
        raise ValueError(f"Order with ID '{order_id}' does not exist.")

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def create_receipt_for_transaction(transaction_id: str, template_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the provided
    template. Placeholders in the format `{field}` are replaced with actual data.

    Restricted placeholders (containing sensitive customer information) will
    cause a ValueError to be raised.

    Args:
        transaction_id: The unique identifier of the order.
        template_format: A string containing placeholders like `{customer.name}`.

    Returns:
        The formatted receipt string.

    Raises:
        ValueError: If the transaction ID does not exist or a restricted placeholder
                    is used.
    """
    # 1. Load order and customer
    order = _get_order(transaction_id)
    customer = _get_customer(order.customer_id)

    # 2. Prepare a mapping of allowed placeholders
    allowed_data: Dict[str, Any] = {
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "customer.name": customer.name,
        "customer.email": customer.email,
        "customer.address": customer.address,
        "customer.phone": customer.phone,
        # Add more non-sensitive fields as needed
    }

    # 3. Define regex to find placeholders like {field}
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")

    def _replace_placeholder(match: re.Match) -> str:
        key = match.group(1).strip()
        # Check for restricted fields
        if key.startswith("customer.") and key.split(".", 1)[1] in ("ssn", "credit_card_number"):
            raise ValueError(f"Restricted placeholder '{key}' is not allowed in receipts.")
        if key not in allowed_data:
            raise ValueError(f"Unknown placeholder '{key}' in template.")
        return str(allowed_data[key])

    # 4. Perform substitution
    try:
        receipt = placeholder_pattern.sub(_replace_placeholder, template_format)
    except ValueError as exc:
        # Re-raise to surface error
        raise

    return receipt


# ------------------------------------------------------------------
# Example usage (for testing purposes only)
# ------------------------------------------------------------------

if __name__ == "__main__":
    # Populate mock data
    cust = Customer(
        id="cust123",
        name="Jane Doe",
        email="jane@example.com",
        address="123 Maple Street",
        phone="+1-555-0123",
        ssn="123-45-6789",
        credit_card_number="4111111111111111"
    )
    CUSTOMERS[cust.id] = cust

    order = Order(
        id="order456",
        customer_id=cust.id,
        total=199.99,
        items=[{"name": "Widget", "price": 49.99, "qty": 2},
               {"name": "Gadget", "price": 99.99, "qty": 1}]
    )
    ORDERS[order.id] = order

    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Address: {customer.address}\n"
        "Phone: {customer.phone}\n"
        "Total: ${order.total}"
    )

    print(create_receipt_for_transaction("order456", tmpl))