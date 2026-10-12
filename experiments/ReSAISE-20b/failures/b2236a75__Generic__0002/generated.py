import re
from typing import Any

# --------------------------------------------------------------------
# Mock data structures – in a real system these would be replaced by
# database models or ORM objects.
# --------------------------------------------------------------------
class Customer:
    def __init__(self, customer_id: str, name: str, email: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email

class Order:
    def __init__(self, order_id: str, total: float, customer: Customer):
        self.order_id = order_id
        self.total = total
        self.customer = customer

# Simple in‑memory registries for the purpose of this example.
CUSTOMERS = {
    "C001": Customer("C001", "Alice Smith", "alice@example.com"),
}
ORDERS = {
    "O1001": Order("O1001", 129.99, CUSTOMERS["C001"]),
}

# --------------------------------------------------------------------
# Helper utilities
# --------------------------------------------------------------------
PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

# Attributes that are considered sensitive and must not be exposed.
SENSITIVE_ATTRIBUTES = {
    "customer.password",
    "order.credit_card_number",
    "order.payment_token",
}

def _resolve_placeholder(obj: Any, path: str) -> Any:
    """
    Resolve a dotted attribute path on an object. Raises ValueError
    if the path is not safe or does not exist.
    """
    # Reject paths that refer to disallowed sensitive data
    if path in SENSITIVE_ATTRIBUTES:
        raise ValueError(f"Access to sensitive attribute '{path}' is prohibited")

    parts = path.split(".")
    current = obj
    for part in parts:
        if not hasattr(current, part):
            raise ValueError(f"Attribute '{part}' not found in object of type {type(current).__name__}")
        current = getattr(current, part)
    return current

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def generate_customer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order using the supplied template.

    The template may contain placeholders of the form `{order.attribute}` or
    `{customer.attribute}`, which will be replaced by the corresponding values.

    Raises:
        ValueError: If the order does not exist, a placeholder refers to an
                    unknown attribute, or access to sensitive data is attempted.
    """
    # 1. Retrieve the order and customer objects
    order = ORDERS.get(order_id)
    if not order:
        raise ValueError(f"Order with ID '{order_id}' not found")

    customer = order.customer
    if not customer:
        raise ValueError(f"Order '{order_id}' has no associated customer")

    # 2. Replace placeholders
    def _replacement(match: re.Match) -> str:
        placeholder = match.group(1)
        try:
            if placeholder.startswith("order."):
                value = _resolve_placeholder(order, placeholder)
            elif placeholder.startswith("customer."):
                value = _resolve_placeholder(customer, placeholder)
            else:
                raise ValueError(f"Unsupported placeholder '{placeholder}'")
        except ValueError as exc:
            # Propagate the error
            raise exc

        # Convert non-string values to string for insertion
        return str(value)

    try:
        receipt = PLACEHOLDER_RE.sub(_replacement, template)
    except ValueError as exc:
        # Re‑raise to signal failure
        raise ValueError(f"Failed to generate receipt: {exc}") from exc

    return receipt

# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = (
#         "Receipt for Order {order.order_id}\n"
#         "Customer: {customer.name} ({customer.email})\n"
#         "Total: ${order.total:.2f}\n"
#     )
#     print(generate_customer_receipt("O1001", tmpl))