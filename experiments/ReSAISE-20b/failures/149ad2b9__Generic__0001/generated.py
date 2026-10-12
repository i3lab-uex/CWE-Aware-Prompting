import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------
# Mock data models (in a real system these would be ORM models)
# --------------------------------------------------------------------

@dataclass
class Customer:
    id: str
    name: str
    email: str
    phone: str
    # Potentially sensitive fields that must not be exposed in receipts
    ssn: str = field(repr=False, default="")  # hidden from repr for safety

@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: list[str]

# --------------------------------------------------------------------
# In‑memory data store for demonstration purposes
# --------------------------------------------------------------------

CUSTOMERS: Dict[str, Customer] = {
    "c001": Customer(id="c001", name="Alice Smith", email="alice@example.com",
                      phone="+1234567890", ssn="111-22-3333"),
    "c002": Customer(id="c002", name="Bob Jones", email="bob@example.com",
                      phone="+0987654321", ssn="444-55-6666"),
}

ORDERS: Dict[str, Order] = {
    "o1001": Order(id="o1001", customer_id="c001", total=150.75,
                   items=["Widget A", "Widget B"]),
    "o1002": Order(id="o1002", customer_id="c002", total=89.99,
                   items=["Gadget X"]),
}

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------

def _get_order(order_id: str) -> Order:
    """Retrieve an order by ID or raise ValueError."""
    try:
        return ORDERS[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' does not exist.") from exc

def _get_customer(customer_id: str) -> Customer:
    """Retrieve a customer by ID or raise ValueError."""
    try:
        return CUSTOMERS[customer_id]
    except KeyError as exc:
        raise ValueError(f"Customer ID '{customer_id}' does not exist.") from exc

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def create_receipt_for_transaction(transaction_id: str, template_format: str) -> str:
    """
    Generate a formatted receipt by substituting placeholders in the
    template with data from the specified transaction.

    Parameters:
        transaction_id (str): Unique order identifier.
        template_format (str): Receipt template containing placeholders.

    Returns:
        str: The fully formatted receipt string.

    Raises:
        ValueError: If the transaction ID is invalid or if a placeholder
                    requests restricted data.
    """
    # Fetch order and customer data
    order = _get_order(transaction_id)
    customer = _get_customer(order.customer_id)

    # Define allowed placeholders and their corresponding values
    allowed_fields = {
        "customer.name": customer.name,
        "customer.email": customer.email,
        "customer.phone": customer.phone,
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "order.items": ", ".join(order.items),
    }

    # Regular expression to find placeholders like {customer.name}
    placeholder_pattern = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

    def replace_match(match: re.Match) -> str:
        key = match.group(1)
        if key not in allowed_fields:
            raise ValueError(f"Unauthorized or unknown placeholder: '{key}'.")
        return allowed_fields[key]

    # Perform substitution
    try:
        receipt = placeholder_pattern.sub(replace_match, template_format)
    except re.error as exc:  # catch malformed regex if any
        raise ValueError("Invalid template format.") from exc

    return receipt

# --------------------------------------------------------------------
# Example usage (for testing purposes only)
# --------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Phone: {customer.phone}\n"
        "Items: {order.items}\n"
        "Total: ${order.total}"
    )
    print(create_receipt_for_transaction("o1001", tmpl))