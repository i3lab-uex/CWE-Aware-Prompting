import re
from dataclasses import dataclass, field
from typing import Dict, Any

# ------------------------------------------------------------
# Dummy data models (in a real system these would be ORM models)
# ------------------------------------------------------------

@dataclass
class Customer:
    id: str
    name: str
    email: str
    # protected attribute – accessing this should raise an error
    _internal_code: str = field(repr=False, default="SECRET")

@dataclass
class Order:
    id: str
    customer: Customer
    total: float
    items: list[str]
    status: str

# ------------------------------------------------------------
# In‑memory data store (for demo purposes)
# ------------------------------------------------------------

CUSTOMERS: Dict[str, Customer] = {
    "c001": Customer(id="c001", name="Alice Smith", email="alice@example.com"),
    "c002": Customer(id="c002", name="Bob Jones", email="bob@example.com"),
}

ORDERS: Dict[str, Order] = {
    "o1001": Order(id="o1001", customer=CUSTOMERS["c001"], total=120.50, items=["Book", "Pen"], status="Shipped"),
    "o1002": Order(id="o1002", customer=CUSTOMERS["c002"], total=45.00, items=["Notebook"], status="Processing"),
}

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

def _get_attribute(obj: Any, attr_path: str) -> Any:
    """
    Safely traverse attributes separated by '.'.
    Raises ValueError if a protected attribute (starting with '_') is accessed.
    """
    parts = attr_path.split(".")
    current_obj = obj
    for part in parts:
        if part.startswith("_"):
            raise ValueError(f"Access to protected attribute '{part}' is forbidden.")
        if not hasattr(current_obj, part):
            raise ValueError(f"Attribute '{part}' not found in object of type {type(current_obj).__name__}.")
        current_obj = getattr(current_obj, part)
    return current_obj

# ------------------------------------------------------------
# Main function
# ------------------------------------------------------------

def create_transaction_receipt(transaction_id: str, temp_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the provided template.

    Parameters
    ----------
    transaction_id : str
        The identifier of the order.
    temp_format : str
        Template string containing placeholders like '{customer.name}' or '{order.total}'.

    Returns
    -------
    str
        The formatted receipt string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the transaction ID is invalid or if a protected attribute is accessed.
    """
    # Validate order existence
    if transaction_id not in ORDERS:
        raise ValueError(f"Invalid transaction ID: {transaction_id}")

    order = ORDERS[transaction_id]
    customer = order.customer

    # Function to replace placeholders
    def _replace(match: re.Match) -> str:
        placeholder = match.group(1)
        try:
            if placeholder.startswith("customer."):
                value = _get_attribute(customer, placeholder[len("customer.") :])
            elif placeholder.startswith("order."):
                value = _get_attribute(order, placeholder[len("order.") :])
            else:
                raise ValueError(f"Unknown placeholder prefix in '{placeholder}'.")
        except ValueError as exc:
            raise ValueError(f"Error processing placeholder '{{{placeholder}}}': {exc}") from exc
        return str(value)

    # Perform substitution
    receipt = PLACEHOLDER_RE.sub(_replace, temp_format)
    return receipt

# ------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Items: {order.items}\n"
        "Total: ${order.total:.2f}\n"
        "Status: {order.status}"
    )
    try:
        print(create_transaction_receipt("o1001", template))
    except ValueError as e:
        print(f"Error: {e}")