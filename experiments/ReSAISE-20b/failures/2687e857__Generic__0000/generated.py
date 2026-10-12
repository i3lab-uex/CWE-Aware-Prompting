import re
from typing import Any, Dict

# --------------------------------------------------------------------------- #
#   Helper data structures (mocked for illustration)
# --------------------------------------------------------------------------- #

class Customer:
    """Simple customer model."""
    def __init__(self, name: str, email: str):
        self.name = name          # public
        self.email = email        # public
        self._ssn = "123-45-6789"  # protected


class Order:
    """Simple order model."""
    def __init__(self, order_id: str, customer: Customer, total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total


# Mock database: mapping from order_id to Order instance
ORDER_DB: Dict[str, Order] = {}


def get_order_by_id(order_id: str) -> Order:
    """Retrieve an order from the mock database."""
    if order_id not in ORDER_DB:
        raise ValueError(f"Order ID '{order_id}' does not exist.")
    return ORDER_DB[order_id]


# --------------------------------------------------------------------------- #
#   Receipt generation logic
# --------------------------------------------------------------------------- #

PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_.]*)\}")

def _resolve_placeholder(key: str, context: Dict[str, Any]) -> str:
    """
    Resolve a single placeholder key against the provided context.

    Parameters
    ----------
    key : str
        Placeholder key, e.g. 'customer.name' or 'order.total'.
    context : dict
        Mapping from object names to their instances.

    Returns
    -------
    str
        String representation of the resolved value.

    Raises
    ------
    ValueError
        If attempting to access a protected attribute (starting with '_')
        or if the key is invalid.
    """
    parts = key.split(".")
    if not parts:
        raise ValueError(f"Empty placeholder in template.")

    obj_name = parts[0]
    if obj_name not in context:
        raise ValueError(f"Unknown placeholder object '{obj_name}'.")

    value = context[obj_name]
    for attr in parts[1:]:
        if attr.startswith("_"):
            raise ValueError(f"Access to protected attribute '{attr}' is forbidden.")
        if not hasattr(value, attr):
            raise ValueError(f"Attribute '{attr}' does not exist on {obj_name}.")
        value = getattr(value, attr)

    return str(value)


def create_transaction_receipt(transaction_id: str, temp_format: str) -> str:
    """
    Generate a receipt string for the given transaction.

    Parameters
    ----------
    transaction_id : str
        Identifier of the order.
    temp_format : str
        Template string containing placeholders such as '{customer.name}'.

    Returns
    -------
    str
        Fully formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if placeholders reference protected data.
    """
    # Retrieve order and build context
    order = get_order_by_id(transaction_id)
    context = {
        "order": order,
        "customer": order.customer
    }

    # Find all placeholders and replace them
    def repl(match: re.Match) -> str:
        key = match.group(1)
        return _resolve_placeholder(key, context)

    try:
        receipt = PLACEHOLDER_RE.sub(repl, temp_format)
    except ValueError as exc:
        raise ValueError(f"Receipt generation failed: {exc}") from None

    return receipt


# --------------------------------------------------------------------------- #
#   Example usage (for testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Populate mock database
    cust = Customer(name="Alice Smith", email="alice@example.com")
    order = Order(order_id="ORD12345", customer=cust, total=149.99)
    ORDER_DB[order.order_id] = order

    template = (
        "Receipt for Order #{order_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total Amount: ${order.total:.2f}\n"
    )

    print(create_transaction_receipt("ORD12345", template))