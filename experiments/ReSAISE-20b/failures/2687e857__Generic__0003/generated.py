import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Mock definitions of Order and Customer used by the function.
# In a real system these would be imported from the application domain.
# ------------------------------------------------------------------
@dataclass
class Customer:
    name: str
    email: str
    _ssn: str = field(repr=False)  # protected attribute, should not be exposed


@dataclass
class Order:
    id: str
    customer: Customer
    total: float
    items: Dict[str, int]  # product_name -> quantity


# ------------------------------------------------------------------
# A simple in-memory store for orders used by the receipt generator.
# In production this would be a database query or service call.
# ------------------------------------------------------------------
_ORDER_STORE: Dict[str, Order] = {}


def register_order(order: Order) -> None:
    """Register an order in the mock store."""
    _ORDER_STORE[order.id] = order


# ------------------------------------------------------------------
# Helper: safe attribute extraction
# ------------------------------------------------------------------
def _safe_getattr(obj, attr_name):
    """
    Retrieve an attribute from an object only if it is not protected
    (doesn't start with '_') and is of a simple serializable type.
    """
    if attr_name.startswith("_"):
        raise ValueError(f"Access to protected attribute '{attr_name}' is forbidden.")
    if not hasattr(obj, attr_name):
        raise ValueError(f"Attribute '{attr_name}' does not exist.")
    value = getattr(obj, attr_name)
    # Allow only basic types for safety
    if isinstance(value, (str, int, float)):
        return value
    raise ValueError(f"Attribute '{attr_name}' is of unsupported type {type(value).__name__}.")


# ------------------------------------------------------------------
# Main function: create_transaction_receipt
# ------------------------------------------------------------------
def create_transaction_receipt(transaction_id: str, temp_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the supplied template.

    Parameters
    ----------
    transaction_id : str
        Identifier of the order.
    temp_format : str
        Template string containing placeholders like '{customer.name}' or '{order.total}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if protected customer information is accessed.
    """
    # Fetch the order; raise error if not found
    order = _ORDER_STORE.get(transaction_id)
    if order is None:
        raise ValueError(f"Invalid transaction ID: {transaction_id}")

    # Regular expression to find placeholders of the form {object.attribute}
    placeholder_pattern = re.compile(r"\{(\w+)\.(\w+)\}")

    def replace_placeholder(match):
        obj_name, attr_name = match.group(1), match.group(2)
        if obj_name == "order":
            source_obj = order
        elif obj_name == "customer":
            source_obj = order.customer
        else:
            raise ValueError(f"Unknown placeholder object '{obj_name}'.")
        return str(_safe_getattr(source_obj, attr_name))

    # Perform replacement safely
    try:
        receipt = placeholder_pattern.sub(replace_placeholder, temp_format)
    except ValueError as e:
        raise ValueError(f"Error generating receipt: {e}") from None

    return receipt


# ------------------------------------------------------------------
# Example usage (for testing purposes)
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Create a customer and order
    cust = Customer(name="Alice Smith", email="alice@example.com", _ssn="123-45-6789")
    ord_ = Order(id="TXN001", customer=cust, total=99.95, items={"Widget": 2, "Gadget": 1})
    register_order(ord_)

    # Define a template
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total}\n"
    )

    # Generate receipt
    print(create_transaction_receipt("TXN001", tmpl))