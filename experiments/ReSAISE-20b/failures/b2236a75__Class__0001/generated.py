import re
from typing import Any, Dict

# ----------------------------------------------------------------------
# Minimal data structures used by the receipt generator.
# In a real system these would be replaced by ORM models or API calls.
# ----------------------------------------------------------------------
class Customer:
    def __init__(self, id: str, name: str, email: str, address: str,
                 ssn: str = None, credit_card: str = None):
        self.id = id
        self.name = name
        self.email = email
        self.address = address
        self.ssn = ssn
        self.credit_card = credit_card


class Order:
    def __init__(self, id: str, total: float, date: str,
                 customer_id: str, payment_info: Dict[str, Any] = None):
        self.id = id
        self.total = total
        self.date = date
        self.customer_id = customer_id
        self.payment_info = payment_info or {}


# ----------------------------------------------------------------------
# In-memory "database" – replace with real persistence in production.
# ----------------------------------------------------------------------
CUSTOMERS = {
    'c001': Customer('c001', 'Alice Smith', 'alice@example.com',
                     '123 Maple St, Townsville', ssn='111-22-3333'),
    'c002': Customer('c002', 'Bob Jones', 'bob@example.com',
                     '456 Oak Ave, Villagetown'),
}

ORDERS = {
    'o1001': Order('o1001', 150.75, '2024-07-20', 'c001',
                   payment_info={'method': 'Credit Card', 'last4': '4242'}),
    'o1002': Order('o1002', 42.00, '2024-07-21', 'c002'),
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_attr_chain(obj: Any, attr_chain: str) -> Any:
    """
    Safely traverse an attribute chain like 'order.total' or
    'customer.address'.
    """
    attrs = attr_chain.split('.')
    current = obj
    for a in attrs:
        if not hasattr(current, a):
            raise AttributeError(f"Attribute '{a}' not found in {current!r}")
        current = getattr(current, a)
    return current


def _build_context(order: Order, customer: Customer) -> Dict[str, Any]:
    """
    Build a flat dictionary that maps placeholder names to values.
    Only whitelisted attributes are included.
    """
    context = {
        'order.id': order.id,
        'order.total': f"{order.total:.2f}",
        'order.date': order.date,
        # Expose only non-sensitive payment info
        'order.payment_method': order.payment_info.get('method', ''),
    }
    # Customer data – only non-sensitive fields
    context.update({
        'customer.id': customer.id,
        'customer.name': customer.name,
        'customer.email': customer.email,
        'customer.address': customer.address,
    })
    return context


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_customer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order using the supplied
    template. The template may contain placeholders such as
    '{order.total}' or '{customer.name}'. Only non-sensitive fields are
    allowed; attempts to access sensitive data will raise ValueError.

    Parameters:
        order_id (str): Identifier of the order.
        template (str): Receipt template string.

    Returns:
        str: The formatted receipt.

    Raises:
        ValueError: If the order_id is invalid, the template contains
                    disallowed placeholders, or an error occurs during
                    formatting.
    """
    # Retrieve objects – in a real system this would involve database lookups
    order = ORDERS.get(order_id)
    if not order:
        raise ValueError(f"Order ID '{order_id}' does not exist")

    customer = CUSTOMERS.get(order.customer_id)
    if not customer:
        raise ValueError(f"Customer ID '{order.customer_id}' does not exist")

    # Build context with whitelisted attributes
    context = _build_context(order, customer)

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r'\{([a-zA-Z_][\w\.]*)\}')
    placeholders = placeholder_pattern.findall(template)

    # Verify each placeholder is allowed
    for ph in placeholders:
        if ph not in context:
            # Reject access to any attribute not explicitly exposed
            raise ValueError(f"Disallowed or unknown placeholder: '{ph}'")

    try:
        # Perform safe formatting
        receipt = template.format(**context)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Error formatting receipt: {exc}") from exc

    return receipt


# ----------------------------------------------------------------------
# Example usage (commented out – remove to run)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Date: {order.date}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Address: {customer.address}\n"
        "Total: ${order.total}\n"
        "Payment Method: {order.payment_method}"
    )
    print(generate_customer_receipt('o1001', tmpl))