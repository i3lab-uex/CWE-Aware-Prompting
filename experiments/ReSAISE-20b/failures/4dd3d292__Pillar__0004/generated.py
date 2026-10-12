import datetime
from typing import Dict, Any

# --------------------------------------------------------------------
# Mock data structures and in‑memory store (replace with real DB access)
# --------------------------------------------------------------------

class Customer:
    def __init__(self, customer_id: str, name: str, email: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        # Protected attribute – should not be exposed in the receipt
        self._credit_score = 750

class Order:
    def __init__(self, order_id: str, customer: Customer,
                 items: Dict[str, int], total: float):
        self.order_id = order_id
        self.customer = customer
        self.items = items          # e.g., {"apple": 2, "banana": 3}
        self.total = total
        self.created_at = datetime.datetime.utcnow()

# In‑memory store of orders keyed by order_id
ORDER_STORE: Dict[str, Order] = {}

# --------------------------------------------------------------------
# Helper utilities
# --------------------------------------------------------------------

def _get_order(order_id: str) -> Order:
    """Retrieve an order from the store, raising ValueError if missing."""
    try:
        return ORDER_STORE[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' does not exist.") from exc

def _extract_safe_attributes(obj: Any, prefix: str = "") -> Dict[str, Any]:
    """
    Recursively extract attributes of an object that are *not* protected
    (i.e., do not start with an underscore). Nested objects are flattened
    using dot‑notation (e.g., 'customer.name').
    """
    attrs = {}
    for attr_name in dir(obj):
        if attr_name.startswith("_"):
            continue  # Skip protected/private attributes
        value = getattr(obj, attr_name)
        key = f"{prefix}{attr_name}" if prefix else attr_name
        # For simple types, store directly; otherwise recurse.
        if isinstance(value, (str, int, float, bool)):
            attrs[key] = value
        elif isinstance(value, dict):
            # Flatten dictionary items with key prefixes
            for k, v in value.items():
                attrs[f"{key}.{k}"] = v
        else:
            # Recurse into nested objects (e.g., customer)
            attrs.update(_extract_safe_attributes(value, f"{key}."))
    return attrs

# --------------------------------------------------------------------
# Core function
# --------------------------------------------------------------------

def create_purchase_receipt(order_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given order.

    Parameters
    ----------
    order_id : str
        Identifier of the order to retrieve.
    receipt_template : str
        Template string containing placeholders such as '{customer.name}'
        or '{order.total}'.

    Returns
    -------
    str
        The fully formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if the template attempts to access
        protected (private) attributes.
    """
    # 1. Retrieve the order safely
    order = _get_order(order_id)

    # 2. Build a flat mapping of safe attributes
    context: Dict[str, Any] = {}
    # Top‑level order fields
    context.update(_extract_safe_attributes(order, prefix="order."))
    # Nested customer fields
    context.update(_extract_safe_attributes(order.customer, prefix="customer."))

    # 3. Validate that all placeholders in the template refer to allowed keys
    # We'll use a simple regex to find all {key} occurrences.
    import re
    placeholder_pattern = r"{([^{}]+)}"
    placeholders = set(re.findall(placeholder_pattern, receipt_template))

    for placeholder in placeholders:
        if placeholder not in context:
            raise ValueError(
                f"Template references invalid or protected attribute '{placeholder}'."
            )

    # 4. Perform formatting using the safe context
    try:
        receipt = receipt_template.format(**context)
    except KeyError as exc:
        # This should not happen due to earlier validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return receipt

# --------------------------------------------------------------------
# Example usage (for testing; remove or comment out in production)
# --------------------------------------------------------------------

if __name__ == "__main__":
    # Create sample data
    cust = Customer("C001", "Alice Smith", "alice@example.com")
    order = Order(
        "O123",
        cust,
        items={"Laptop": 1, "Mouse": 2},
        total=1299.99,
    )
    ORDER_STORE[order.order_id] = order

    # Define a receipt template
    tmpl = (
        "Receipt for Order {order.order_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Items:\n"
        "  - Laptop: 1\n"
        "  - Mouse: 2\n"
        "Total: ${order.total:.2f}\n"
        "Date: {order.created_at:%Y-%m-%d %H:%M:%S}"
    )

    print(create_purchase_receipt("O123", tmpl))