import re
from dataclasses import dataclass, field
from typing import Dict, Any

# -------------------- Domain Models ------------------------------------

@dataclass
class Customer:
    """Simple customer model."""
    id: str
    name: str
    email: str
    phone: str
    # Sensitive / restricted attributes
    password: str = field(repr=False, default="")  # never expose

@dataclass
class Order:
    """Simple order model."""
    id: str
    customer_id: str
    total: float
    items: list[str]
    shipping_address: str

# -------------------- In‑memory Store ---------------------------------

class OrderStore:
    """A minimal in-memory repository for orders and customers."""
    _orders: Dict[str, Order] = {}
    _customers: Dict[str, Customer] = {}

    @classmethod
    def add_customer(cls, customer: Customer) -> None:
        cls._customers[customer.id] = customer

    @classmethod
    def add_order(cls, order: Order) -> None:
        cls._orders[order.id] = order

    @classmethod
    def get_order(cls, order_id: str) -> Order:
        if order_id not in cls._orders:
            raise KeyError(f"Order {order_id} not found")
        return cls._orders[order_id]

    @classmethod
    def get_customer(cls, customer_id: str) -> Customer:
        if customer_id not in cls._customers:
            raise KeyError(f"Customer {customer_id} not found")
        return cls._customers[customer_id]

# -------------------- Receipt Generation --------------------------------

PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

# List of attributes that are considered protected and must not be exposed
RESTRICTED_FIELDS = {"customer.password", "customer.ssn"}

def _get_attr_value(obj: Any, attr_path: str) -> Any:
    """
    Resolve a dotted attribute path on an object.
    Raises AttributeError if any part of the path is missing.
    """
    parts = attr_path.split(".")
    current = obj
    for part in parts:
        if not hasattr(current, part):
            raise AttributeError(f"Attribute '{part}' missing in {current}")
        current = getattr(current, part)
    return current

def create_receipt_for_transaction(transaction_id: str, template_format: str) -> str:
    """
    Generate a receipt by substituting placeholders in `template_format`
    with actual order and customer data.

    Parameters
    ----------
    transaction_id : str
        The unique identifier of the order.
    template_format : str
        Template string containing placeholders such as `{customer.name}`.

    Returns
    -------
    str
        The formatted receipt string with placeholders replaced.

    Raises
    ------
    ValueError
        If the order ID does not exist or if a placeholder requests
        restricted data from the customer.
    """
    # Retrieve order and associated customer safely
    try:
        order = OrderStore.get_order(transaction_id)
        customer = OrderStore.get_customer(order.customer_id)
    except KeyError as exc:
        raise ValueError(str(exc)) from None

    # Function to replace each placeholder
    def _replace(match: re.Match) -> str:
        key = match.group(1)

        # Reject any placeholder that accesses protected data
        if key in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{key}' is not allowed")

        # Resolve value based on prefix
        try:
            if key.startswith("customer."):
                value = _get_attr_value(customer, key[len("customer.") :])
            elif key.startswith("order."):
                value = _get_attr_value(order, key[len("order.") :])
            else:
                raise ValueError(f"Unknown placeholder prefix in '{key}'")
        except AttributeError as exc:
            raise ValueError(f"Invalid placeholder '{key}': {exc}") from None

        # Convert non-string values to string
        return str(value)

    # Perform substitution
    try:
        receipt = PLACEHOLDER_RE.sub(_replace, template_format)
    except ValueError as exc:
        raise  # propagate the same exception

    return receipt

# -------------------- Example Usage ------------------------------------

if __name__ == "__main__":
    # Setup mock data
    cust = Customer(id="c1", name="Alice Smith", email="alice@example.com",
                    phone="+1234567890", password="secret")
    OrderStore.add_customer(cust)

    order = Order(id="o1", customer_id="c1", total=149.99,
                  items=["Laptop", "Mouse"], shipping_address="123 Main St")
    OrderStore.add_order(order)

    template = (
        "Receipt for Order #{order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total}\n"
        "Items: {order.items}\n"
        "Shipping Address: {order.shipping_address}"
    )

    print(create_receipt_for_transaction("o1", template))