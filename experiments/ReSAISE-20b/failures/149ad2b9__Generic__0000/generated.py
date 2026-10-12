import re
from datetime import datetime
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Mock data models – in a real system these would be ORM entities or API calls
# --------------------------------------------------------------------------- #
class Customer:
    def __init__(self, customer_id: str, name: str, email: str, phone: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

class Order:
    def __init__(self, order_id: str, customer: Customer,
                 total: float, items: list, date: datetime):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items            # list of dicts with item details
        self.date = date

# --------------------------------------------------------------------------- #
# In‑memory data store for demonstration purposes
# --------------------------------------------------------------------------- #
CUSTOMERS: Dict[str, Customer] = {
    "C001": Customer("C001", "Alice Smith", "alice@example.com", "+123456789"),
    "C002": Customer("C002", "Bob Johnson", "bob@example.com", "+987654321"),
}

ORDERS: Dict[str, Order] = {
    "O1001": Order(
        "O1001",
        CUSTOMERS["C001"],
        total=149.99,
        items=[
            {"name": "Widget A", "qty": 2, "price": 49.99},
            {"name": "Widget B", "qty": 1, "price": 49.99},
        ],
        date=datetime(2024, 7, 20, 14, 30),
    ),
    "O1002": Order(
        "O1002",
        CUSTOMERS["C002"],
        total=89.50,
        items=[
            {"name": "Gadget X", "qty": 1, "price": 89.50},
        ],
        date=datetime(2024, 7, 21, 9, 15),
    ),
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def get_order_by_id(order_id: str) -> Order:
    """Retrieve an order by its ID or raise ValueError if not found."""
    try:
        return ORDERS[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' does not exist.") from exc

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def create_receipt_for_transaction(transaction_id: str, template_format: str) -> str:
    """
    Generate a receipt string by replacing placeholders in the provided template
    with data from the order and its associated customer.

    Allowed placeholders:
        {customer.name}
        {customer.email}
        {customer.phone}
        {order.id}
        {order.total}
        {order.date}  (ISO format)
        {order.items} (JSON string)

    Raises:
        ValueError: if the transaction ID is unknown or a placeholder requests
                    restricted data.
    """
    # Retrieve order
    order = get_order_by_id(transaction_id)

    # Define allowed fields mapping to actual values
    context: Dict[str, Any] = {
        "customer.name": order.customer.name,
        "customer.email": order.customer.email,
        "customer.phone": order.customer.phone,
        "order.id": order.order_id,
        "order.total": f"${order.total:,.2f}",
        "order.date": order.date.isoformat(),
        # items will be rendered as a simple string list
        "order.items": "\n".join(
            f"- {item['name']} (Qty: {item['qty']}, Unit: ${item['price']:,.2f})"
            for item in order.items
        ),
    }

    # Regex to find all placeholders like {something}
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")

    def replace_placeholder(match: re.Match) -> str:
        key = match.group(1).strip()
        if key not in context:
            # Reject any placeholder that is not explicitly allowed
            raise ValueError(f"Restricted or unknown placeholder: '{{{key}}}'")
        return str(context[key])

    # Perform substitution
    try:
        receipt = placeholder_pattern.sub(replace_placeholder, template_format)
    except ValueError as exc:
        # Re‑raise with context
        raise ValueError(str(exc)) from None

    return receipt

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Date: {order.date}\n\n"
        "Customer:\n"
        "  Name: {customer.name}\n"
        "  Email: {customer.email}\n"
        "  Phone: {customer.phone}\n\n"
        "Items:\n{order.items}\n\n"
        "Total: {order.total}"
    )
    print(create_receipt_for_transaction("O1001", tmpl))