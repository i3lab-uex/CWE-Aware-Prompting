import re

# Assume these classes are provided by the e‑commerce application.
# They should expose public attributes that can be accessed for receipt generation.
from typing import Any, Dict

class Order:
    """Placeholder – in the real system this would be fully implemented."""
    def __init__(self, order_id: str, customer: "Customer", total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total

class Customer:
    """Placeholder – in the real system this would be fully implemented."""
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

# --------------------------------------------------------------------------- #
# Mock data store – in production this would be replaced with a database call
ORDERS_DB: Dict[str, Order] = {}

def get_order_by_id(order_id: str) -> Order:
    """Retrieve an order from the data store or raise ValueError if not found."""
    order = ORDERS_DB.get(order_id)
    if not order:
        raise ValueError(f"Order ID '{order_id}' does not exist.")
    return order

# --------------------------------------------------------------------------- #
def generate_client_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt for the given order using the supplied template.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        Receipt template containing placeholders such as '{customer.name}' or
        '{order.total}'. Only these two namespaces are allowed.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if an attempt is made to access
        restricted customer data.
    """
    # 1. Retrieve the order
    order = get_order_by_id(order_id)

    # 2. Validate template placeholders – only allow 'customer' and 'order'
    placeholder_pattern = re.compile(r"\{([a-zA-Z_][\w]*)\.([a-zA-Z_][\w]*)\}")
    for full_match, namespace, attr in placeholder_pattern.findall(template):
        if namespace not in {"customer", "order"}:
            raise ValueError(f"Disallowed placeholder '{{{namespace}.{attr}}}' in template.")
        # Check that the attribute exists on the object
        obj = order.customer if namespace == "customer" else order
        if not hasattr(obj, attr):
            raise ValueError(f"Attribute '{attr}' not found on {namespace} object.")

    # 3. Build a mapping for format()
    context = {
        "customer": order.customer,
        "order": order
    }

    try:
        receipt = template.format(**context)
    except (KeyError, AttributeError) as exc:
        # This should not happen due to earlier checks but guard anyway
        raise ValueError(f"Failed to format receipt: {exc}") from exc

    return receipt


# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    # Populate mock database
    cust = Customer(name="Alice Smith", email="alice@example.com")
    ORDERS_DB["12345"] = Order(order_id="12345", customer=cust, total=149.99)

    tmpl = (
        "Hello {customer.name},\n"
        "Thank you for your purchase!\n"
        "Order ID: {order.order_id}\n"
        "Total: ${order.total:.2f}\n"
        "We hope you enjoy your items."
    )

    print(generate_client_receipt("12345", tmpl))