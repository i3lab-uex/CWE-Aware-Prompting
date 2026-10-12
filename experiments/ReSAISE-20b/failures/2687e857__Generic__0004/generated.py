import re
from typing import Dict

# ----------------------------------------------------------------------
# Minimal data model for demonstration purposes.
# In a real application these would be replaced by ORM models or services.
# ----------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        # protected attribute that should not be exposed via the template
        self._ssn = "123-45-6789"

class Order:
    def __init__(self, order_id: str, customer: Customer,
                 items: Dict[str, int], total: float):
        self.order_id = order_id
        self.customer = customer
        self.items = items          # e.g. {"widget": 2, "gadget": 1}
        self.total = total

# ----------------------------------------------------------------------
# In‑memory store of orders (acting as a stand‑in for a database)
# ----------------------------------------------------------------------
ORDERS: Dict[str, Order] = {}

def _populate_demo_data() -> None:
    """Populate the ORDERS dict with a single demo order."""
    cust = Customer(name="Alice Smith", email="alice@example.com")
    ORDERS["TXN-001"] = Order(
        order_id="TXN-001",
        customer=cust,
        items={"widget": 2, "gadget": 1},
        total=59.99,
    )

# Ensure demo data is available
_populate_demo_data()

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_attr_by_path(obj, path: str):
    """
    Retrieve nested attributes from an object using dot notation.
    Raises AttributeError if any part of the path is missing or protected.
    """
    parts = path.split(".")
    for part in parts:
        # Prevent access to protected attributes
        if part.startswith("_"):
            raise AttributeError(f"Access to protected attribute '{part}' is forbidden.")
        if not hasattr(obj, part):
            raise AttributeError(f"Attribute '{part}' not found on object {obj}.")
        obj = getattr(obj, part)
    return obj

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_transaction_receipt(transaction_id: str, temp_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the provided
    template. Placeholders in the template are of the form `{field}` where
    `field` may refer to nested attributes using dot notation (e.g.
    `{customer.name}`).

    Parameters
    ----------
    transaction_id : str
        The identifier of the order.
    temp_format : str
        Template string containing placeholders.

    Returns
    -------
    str
        The formatted receipt string with all placeholders replaced by the
        corresponding order data.

    Raises
    ------
    ValueError
        If the transaction ID is invalid or if a placeholder refers to a
        protected attribute.
    """
    # Validate transaction ID
    order = ORDERS.get(transaction_id)
    if order is None:
        raise ValueError(f"Invalid transaction ID: {transaction_id}")

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^\}]+)\}")
    placeholders = placeholder_pattern.findall(temp_format)

    # Build a mapping from placeholder to value
    replacements: Dict[str, str] = {}
    for key in placeholders:
        try:
            value = _get_attr_by_path(order, key)
        except AttributeError as exc:
            raise ValueError(f"Invalid placeholder '{key}': {exc}") from None
        # Convert non-string values to string for formatting
        replacements[key] = str(value)

    # Perform the replacement safely
    def _replace(match: re.Match) -> str:
        key = match.group(1)
        return replacements.get(key, match.group(0))

    receipt = placeholder_pattern.sub(_replace, temp_format)
    return receipt

# ----------------------------------------------------------------------
# Example usage
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Receipt for Order {order_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Items:\n"
        "{items}\n"
        "Total: ${order.total:.2f}"
    )

    # Convert items dict to a readable string
    def format_items(order: Order) -> str:
        return "\n".join(f"  - {k}: {v}" for k, v in order.items.items())

    # Generate receipt
    try:
        receipt = create_transaction_receipt("TXN-001", template)
        # Replace the {items} placeholder manually since it's a dict
        receipt = receipt.replace("{items}", format_items(ORDERS["TXN-001"]))
        print(receipt)
    except ValueError as e:
        print(f"Error: {e}")