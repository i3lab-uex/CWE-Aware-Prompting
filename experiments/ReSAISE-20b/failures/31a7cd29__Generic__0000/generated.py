import re
from typing import Dict

# --- Minimal data model (would normally be provided elsewhere) -----------------

class Customer:
    """Represents a customer."""
    __slots__ = ("id", "name", "address", "phone")

    def __init__(self, id: str, name: str, address: str, phone: str):
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone


class Order:
    """Represents an order."""
    __slots__ = ("id", "customer", "total", "items")

    def __init__(self, id: str, customer: Customer, total: float, items: list):
        self.id = id
        self.customer = customer
        self.total = total
        self.items = items


# --- Simulated persistence layer ---------------------------------------------

# In a real application this would be replaced by database access.
ORDERS_DB: Dict[str, Order] = {}

def register_order(order: Order):
    """Helper to populate the simulated DB."""
    ORDERS_DB[order.id] = order


# --- Core implementation -------------------------------------------------------

ALLOWED_CUSTOMER_FIELDS = {"name", "address", "phone"}
ALLOWED_ORDER_FIELDS = {"id", "total"}

PLACEHOLDER_PATTERN = re.compile(r"\{(?P<obj>\w+)\.(?P<attr>[\w\.]+)\}")

def _get_value(obj: object, attr_path: str):
    """Retrieve nested attribute safely."""
    parts = attr_path.split(".")
    value = obj
    for part in parts:
        if not hasattr(value, part):
            raise ValueError(f"Attribute '{part}' does not exist on object of type {type(value).__name__}")
        value = getattr(value, part)
    return value

def build_order_receipt(order_identifier: str, template_string: str) -> str:
    """
    Build a receipt string by replacing placeholders with actual data.

    :param order_identifier: Unique identifier of the order.
    :param template_string: Receipt template containing placeholders like
                            '{customer.name}' or '{order.total}'.
    :return: The formatted receipt string.
    :raises ValueError: If the order does not exist or a placeholder refers
                        to restricted data.
    """
    # Fetch the order; raise error if missing
    order = ORDERS_DB.get(order_identifier)
    if order is None:
        raise ValueError(f"Order ID '{order_identifier}' does not exist.")

    # Helper to resolve a single placeholder
    def replace_placeholder(match: re.Match) -> str:
        obj_name = match.group("obj")
        attr_path = match.group("attr")

        if obj_name == "customer":
            # Ensure the attribute is allowed
            root_attr = attr_path.split(".")[0]
            if root_attr not in ALLOWED_CUSTOMER_FIELDS:
                raise ValueError(f"Access to restricted customer attribute '{attr_path}' is not allowed.")
            value = _get_value(order.customer, attr_path)
        elif obj_name == "order":
            root_attr = attr_path.split(".")[0]
            if root_attr not in ALLOWED_ORDER_FIELDS:
                raise ValueError(f"Access to restricted order attribute '{attr_path}' is not allowed.")
            value = _get_value(order, attr_path)
        else:
            raise ValueError(f"Unknown placeholder object '{obj_name}'.")
        return str(value)

    # Perform the substitution
    try:
        receipt = PLACEHOLDER_PATTERN.sub(replace_placeholder, template_string)
    except ValueError as exc:
        # Re‑raise with context
        raise ValueError(f"Failed to build receipt: {exc}") from None

    return receipt


# --- Example usage -------------------------------------------------------------

if __name__ == "__main__":
    # Create a customer and order
    cust = Customer(id="C001", name="Alice Smith", address="123 Maple St.", phone="555-0100")
    order = Order(id="O1001", customer=cust, total=149.99, items=["Widget A", "Gadget B"])
    register_order(order)

    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name}\n"
        "Address: {customer.address}\n"
        "Phone: {customer.phone}\n"
        "Total: ${order.total:.2f}\n"
    )

    print(build_order_receipt("O1001", tmpl))