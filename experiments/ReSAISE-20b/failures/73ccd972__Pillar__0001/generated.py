import re
from typing import Any, Dict

# ----------------------------------------------------------------------
# Mock data models (replace with real implementations in production)
# ----------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, address: str, phone: str):
        self.name = name
        self.address = address
        self.phone = phone
        # Sensitive data that must not be exposed via the template
        self._ssn = "123-45-6789"
        self.email = "customer@example.com"

class Order:
    def __init__(self, purchase_id: str, total: float, customer: Customer):
        self.purchase_id = purchase_id
        self.total = total
        self.customer = customer

# ----------------------------------------------------------------------
# In‑memory store for demo purposes (replace with DB or cache lookup)
# ----------------------------------------------------------------------
_ORDER_DB: Dict[str, Order] = {}

def register_order(order: Order) -> None:
    """Helper to add an order to the in‑memory store."""
    _ORDER_DB[order.purchase_id] = order

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def create_order_receipt(purchase_id: str, receipt_template: str) -> str:
    """
    Generate a receipt by substituting placeholders in the template with
    actual order and customer data.

    Args:
        purchase_id: Unique identifier for the order.
        receipt_template: Template string containing placeholders such as
                          '{customer.name}' and '{order.total}'.

    Returns:
        A formatted receipt string with all placeholders replaced.

    Raises:
        ValueError: If the order ID does not exist or if a placeholder
                    requests restricted data.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve the order (resource acquisition)
    # ------------------------------------------------------------------
    try:
        # Using context manager style to illustrate resource control
        order = _ORDER_DB[purchase_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{purchase_id}' does not exist") from exc

    # ------------------------------------------------------------------
    # 2. Define allowed placeholder fields
    # ------------------------------------------------------------------
    ALLOWED_FIELDS = {
        "order.purchase_id",
        "order.total",
        # Customer public fields
        "customer.name",
        "customer.address",
        "customer.phone",
    }

    # ------------------------------------------------------------------
    # 3. Find all placeholders in the template
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    placeholders = set(placeholder_pattern.findall(receipt_template))

    # ------------------------------------------------------------------
    # 4. Validate placeholders against the whitelist
    # ------------------------------------------------------------------
    for ph in placeholders:
        if ph not in ALLOWED_FIELDS:
            raise ValueError(f"Restricted or unknown placeholder '{ph}'")

    # ------------------------------------------------------------------
    # 5. Build a context dictionary for formatting
    # ------------------------------------------------------------------
    context: Dict[str, Any] = {
        "order.purchase_id": order.purchase_id,
        "order.total": f"{order.total:.2f}",
        "customer.name": order.customer.name,
        "customer.address": order.customer.address,
        "customer.phone": order.customer.phone,
    }

    # ------------------------------------------------------------------
    # 6. Perform substitution safely
    # ------------------------------------------------------------------
    def replace_match(match: re.Match) -> str:
        key = match.group(1)
        return context[key]

    formatted_receipt = placeholder_pattern.sub(replace_match, receipt_template)

    # ------------------------------------------------------------------
    # 7. Return the final receipt
    # ------------------------------------------------------------------
    return formatted_receipt

# ----------------------------------------------------------------------
# Example usage (for demonstration; remove in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    cust = Customer(name="Jane Doe", address="123 Elm St", phone="555-0123")
    order = Order(purchase_id="ORD001", total=99.95, customer=cust)
    register_order(order)

    template = (
        "Receipt for Order #{order.purchase_id}\n"
        "Customer: {customer.name}\n"
        "Address: {customer.address}\n"
        "Phone: {customer.phone}\n"
        "Total Paid: ${order.total}\n"
    )

    print(create_order_receipt("ORD001", template))