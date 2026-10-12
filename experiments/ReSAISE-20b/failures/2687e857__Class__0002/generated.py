import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
# Mock data models (in a real system these would be ORM entities)
# ------------------------------------------------------------------

@dataclass
class Customer:
    id: str
    name: str
    email: str
    # Protected attribute – should not be exposed in receipts
    _ssn: str


@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: list  # list of item descriptions


# ------------------------------------------------------------------
# In‑memory data store (replace with real persistence in production)
# ------------------------------------------------------------------

CUSTOMERS: Dict[str, Customer] = {
    "c001": Customer(id="c001", name="Alice Smith", email="alice@example.com", _ssn="123-45-6789"),
    "c002": Customer(id="c002", name="Bob Jones", email="bob@example.com", _ssn="987-65-4321"),
}

ORDERS: Dict[str, Order] = {
    "o100": Order(id="o100", customer_id="c001", total=49.99, items=["Widget A", "Gadget B"]),
    "o101": Order(id="o101", customer_id="c002", total=79.49, items=["Thingamajig"]),
}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def _get_attribute_chain(obj, attr_chain):
    """
    Resolve a dotted attribute chain on an object.
    Raises ValueError if any intermediate attribute is protected
    (i.e. starts with an underscore).
    """
    current = obj
    for attr in attr_chain:
        if attr.startswith("_"):
            raise ValueError(f"Access to protected attribute '{attr}' is not allowed.")
        if not hasattr(current, attr):
            raise ValueError(f"Attribute '{attr}' does not exist on object of type {type(current).__name__}.")
        current = getattr(current, attr)
    return current

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

def create_transaction_receipt(transaction_id: str, temp_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the supplied template.

    Parameters
    ----------
    transaction_id : str
        Identifier of the order.
    temp_format : str
        Template string containing placeholders such as '{customer.name}' or '{order.total}'.

    Returns
    -------
    str
        The formatted receipt string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the transaction ID is unknown, or if a placeholder refers to a protected attribute.
    """
    # Validate transaction ID
    order = ORDERS.get(transaction_id)
    if not order:
        raise ValueError(f"Invalid transaction ID: {transaction_id}")

    # Resolve the customer object
    customer = CUSTOMERS.get(order.customer_id)
    if not customer:
        raise ValueError(f"Customer with ID {order.customer_id} not found for order {transaction_id}")

    # Prepare a mapping for quick lookup
    context = {
        "order": order,
        "customer": customer,
    }

    def _replace_placeholder(match):
        placeholder = match.group(1)          # e.g. 'customer.name'
        parts = placeholder.split(".")       # ['customer', 'name']
        if not parts:
            return match.group(0)

        base_name = parts[0]
        attr_chain = parts[1:]

        # Resolve the base object
        if base_name not in context:
            raise ValueError(f"Unknown placeholder base '{base_name}' in template.")
        obj = context[base_name]

        # Resolve the attribute chain safely
        value = _get_attribute_chain(obj, attr_chain)
        return str(value)

    # Perform the replacement
    try:
        receipt = PLACEHOLDER_RE.sub(_replace_placeholder, temp_format)
    except ValueError as exc:
        # Re‑raise to caller
        raise

    return receipt

# ------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ------------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Items:\n{order.items}\n"
        "Total: ${order.total:.2f}"
    )
    try:
        print(create_transaction_receipt("o100", template))
    except ValueError as e:
        print(f"Error generating receipt: {e}")