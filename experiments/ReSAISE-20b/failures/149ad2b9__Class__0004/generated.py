import re
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mocked domain classes (replace with the real ones in your project)
# ----------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email
        self.phone = phone   # *Sensitive* – should not be exposed


class Order:
    def __init__(self, transaction_id: str, customer: Customer,
                 total: float, items: list):
        self.transaction_id = transaction_id
        self.customer = customer
        self.total = total
        self.items = items   # e.g., list of dicts with item details


# ----------------------------------------------------------------------
# Simulated data store (replace with real persistence layer)
# ----------------------------------------------------------------------
ORDERS: Dict[str, Order] = {}


def get_order(transaction_id: str) -> Order:
    """
    Retrieve an order from the data store. Raises KeyError if not found.
    """
    return ORDERS[transaction_id]


# ----------------------------------------------------------------------
# Receipt generation
# ----------------------------------------------------------------------
def create_receipt_for_transaction(transaction_id: str, template_format: str) -> str:
    """
    Generates a receipt for the given transaction ID using the supplied template.
    
    Parameters
    ----------
    transaction_id : str
        Unique identifier of the order.
    template_format : str
        Template string containing placeholders like `{customer.name}` or `{order.total}`.
    
    Returns
    -------
    str
        The fully formatted receipt string.
    
    Raises
    ------
    ValueError
        If the order ID does not exist or if a placeholder requests restricted data.
    """
    # 1. Load the order
    try:
        order = get_order(transaction_id)
    except KeyError as exc:
        raise ValueError(f"Order with ID '{transaction_id}' not found.") from exc

    # 2. Define allowed placeholders (whitelist)
    ALLOWED_PLACEHOLDERS = {
        "customer.name",
        "customer.email",
        "order.total",
        "order.items",   # items will be rendered via a custom formatter
    }

    # 3. Prepare the context dictionary for substitution
    context: Dict[str, Any] = {
        "customer.name": order.customer.name,
        "customer.email": order.customer.email,
        "order.total": f"{order.total:.2f}",
    }

    # Custom rendering for items
    def render_items(items):
        lines = []
        for idx, item in enumerate(items, 1):
            # Assume each item dict has 'name' and 'price'
            name = item.get("name", "Unknown")
            price = item.get("price", 0.0)
            lines.append(f"{idx}. {name} - ${price:.2f}")
        return "\n".join(lines)

    context["order.items"] = render_items(order.items)

    # 4. Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    for match in placeholder_pattern.finditer(template_format):
        key = match.group(1).strip()
        if key not in ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Unauthorized or unknown placeholder: '{key}'")
        # Ensure the key exists in context
        if key not in context:
            raise ValueError(f"Missing data for placeholder: '{key}'")

    # 5. Perform the substitution
    try:
        receipt = template_format.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder data: {exc}") from exc

    return receipt


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     cust = Customer(name="Alice Smith", email="alice@example.com", phone="555-1234")
#     order = Order(
#         transaction_id="TXN1001",
#         customer=cust,
#         total=125.50,
#         items=[{"name": "Widget A", "price": 45.00}, {"name": "Widget B", "price": 80.50}]
#     )
#     ORDERS[order.transaction_id] = order
#
#     tmpl = (
#         "Receipt for {customer.name}\n"
#         "Email: {customer.email}\n\n"
#         "Items Purchased:\n{order.items}\n\n"
#         "Total: ${order.total}"
#     )
#
#     print(create_receipt_for_transaction("TXN1001", tmpl))