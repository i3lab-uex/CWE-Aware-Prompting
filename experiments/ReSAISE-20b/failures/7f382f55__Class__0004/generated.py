import re
from typing import Dict

# --------------------------------------------------------------------------- #
# Mocked domain models (in a real system these would be imported from the data layer)
# --------------------------------------------------------------------------- #
class Customer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email  # sensitive

class Order:
    def __init__(self, order_id: str, customer: Customer, total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total

# --------------------------------------------------------------------------- #
# In‑memory repository of orders (replace with a real DB lookup in production)
# --------------------------------------------------------------------------- #
ORDER_DB: Dict[str, Order] = {}

def get_order_by_id(order_id: str) -> Order:
    """Retrieve an order from the repository. Raises ValueError if not found."""
    order = ORDER_DB.get(order_id)
    if order is None:
        raise ValueError(f"Order ID '{order_id}' does not exist.")
    return order

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def compose_invoice_template(invoice_id: str, receipt_format: str) -> str:
    """
    Generate a receipt string by replacing placeholders in `receipt_format`
    with data from the order identified by `invoice_id`.

    Placeholders follow the pattern `{object.attribute}`.
    Access to protected attributes (starting with '_') is prohibited and will
    raise a ValueError. Sensitive data such as customer.email is masked.

    Args:
        invoice_id: Identifier of the order.
        receipt_format: Template string containing placeholders.

    Returns:
        A fully formatted receipt string.

    Raises:
        ValueError: If the order ID is invalid or if a protected attribute
                    is accessed.
    """
    # Fetch order; will raise ValueError if not found
    order = get_order_by_id(invoice_id)

    # Function to resolve a single placeholder
    def _resolve(match: re.Match) -> str:
        full_path = match.group(1).strip()
        parts = full_path.split('.')
        if not parts:
            return ""

        # Resolve the root object
        obj = globals().get(parts[0])
        if obj is None:
            raise ValueError(f"Unknown placeholder root: '{parts[0]}'")

        # Resolve attributes step by step
        for attr in parts[1:]:
            if attr.startswith('_'):
                raise ValueError(f"Access to protected attribute '{attr}' is forbidden.")
            if isinstance(obj, Order):
                if attr == 'customer':
                    obj = obj.customer
                elif attr == 'total':
                    return f"{obj.total:.2f}"
                else:
                    raise ValueError(f"Unknown attribute '{attr}' on Order.")
            elif isinstance(obj, Customer):
                if attr == 'name':
                    return obj.name
                elif attr == 'email':
                    # Mask email to avoid leaking sensitive info
                    local, domain = obj.email.split('@')
                    masked_local = local[0] + '*' * max(len(local)-2, 0) + local[-1]
                    return f"{masked_local}@{domain}"
                else:
                    raise ValueError(f"Unknown attribute '{attr}' on Customer.")
            else:
                raise ValueError(f"Unsupported object type for placeholder resolution.")

        # If we reach here, the last attribute was a string value
        return str(obj)

    # Replace all placeholders in the template
    pattern = re.compile(r'\{([^}]+)\}')
    try:
        receipt = pattern.sub(_resolve, receipt_format)
    except ValueError as exc:
        raise  # re‑raise to propagate the error

    return receipt

# --------------------------------------------------------------------------- #
# Example usage (uncomment for testing)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     cust = Customer(name="Alice Smith", email="alice@example.com")
#     order = Order(order_id="ORD12345", customer=cust, total=199.99)
#     ORDER_DB[order.order_id] = order
#
#     template = (
#         "Invoice #{invoice_id}\n"
#         "Customer: {customer.name}\n"
#         "Email: {customer.email}\n"
#         "Total Due: ${order.total}\n"
#     )
#
#     print(compose_invoice_template("ORD12345", template))