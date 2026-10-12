import re
from typing import Any, Dict

# --------------------------------------------------------------------------- #
#  Mock definitions for Order and Customer classes.
# In a real system these would be imported from the domain layer.
# --------------------------------------------------------------------------- #
class Customer:
    def __init__(self, name: str, email: str, phone: str, ssn: str):
        self.name = name
        self.email = email
        self.phone = phone
        self.ssn = ssn  # Sensitive field

class Order:
    _orders: Dict[str, "Order"] = {}

    def __init__(self, order_id: str, customer: Customer, total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total

    @classmethod
    def get(cls, order_id: str) -> "Order":
        return cls._orders.get(order_id)

    @classmethod
    def add(cls, order: "Order") -> None:
        cls._orders[order.order_id] = order

# --------------------------------------------------------------------------- #
#  Core implementation
# --------------------------------------------------------------------------- #

# List of protected attributes that must not appear in a public receipt.
PROTECTED_FIELDS = {"ssn", "credit_card_number"}

# Regular expression to capture placeholders like {customer.name}
PLACEHOLDER_RE = re.compile(r"\{(?P<path>[^\}]+)\}")

def _extract_value(obj: Any, path: str) -> Any:
    """
    Traverse attributes of `obj` following a dot separated `path`.
    Raises ValueError if any intermediate attribute is missing.
    """
    parts = path.split(".")
    current = obj
    for part in parts:
        if not hasattr(current, part):
            raise ValueError(f"Invalid placeholder: missing attribute '{part}' in path '{path}'.")
        current = getattr(current, part)
    return current

def create_order_receipt(purchase_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt string by replacing placeholders in `receipt_template`
    with actual values from the Order and its associated Customer.

    Parameters
    ----------
    purchase_id : str
        Unique identifier of the order.
    receipt_template : str
        Template containing placeholders such as '{customer.name}' and '{order.total}'.

    Returns
    -------
    str
        The fully formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID does not exist, or if a placeholder references protected data.
    """
    # Retrieve the order
    order = Order.get(purchase_id)
    if not order:
        raise ValueError(f"Order with ID '{purchase_id}' does not exist.")

    # Prepare a mapping for placeholder resolution
    context = {
        "order": order,
        "customer": order.customer,
    }

    # Function to replace each placeholder
    def _replace(match: re.Match) -> str:
        path = match.group("path").strip()
        # Check for protected fields
        if any(part in PROTECTED_FIELDS for part in path.split(".")):
            raise ValueError(f"Attempt to expose protected data: '{path}'.")
        try:
            value = _extract_value(context[path.split(".")[0]], ".".join(path.split(".")[1:]))
        except KeyError:
            raise ValueError(f"Invalid placeholder path '{path}'.")
        return str(value)

    # Perform substitution
    try:
        formatted = PLACEHOLDER_RE.sub(_replace, receipt_template)
    except ValueError as e:
        raise

    return formatted