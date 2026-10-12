import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------------- #
# Mocked domain models (in a real application these would come from the ORM)
# --------------------------------------------------------------------------- #

@dataclass
class User:
    id: str
    name: str
    email: str
    is_restricted: bool = False

@dataclass
class Order:
    id: str
    total: float
    customer: User

# --------------------------------------------------------------------------- #
# In‑memory "database" for demonstration purposes
# --------------------------------------------------------------------------- #

ORDERS_DB: Dict[str, Order] = {}

def _seed_demo_data() -> None:
    """Populate the in‑memory DB with a couple of orders."""
    global ORDERS_DB
    user1 = User(id="u1", name="Alice Smith", email="alice@example.com")
    user2 = User(id="u2", name="Bob Jones", email="bob@example.com", is_restricted=True)

    ORDERS_DB["o1"] = Order(id="o1", total=123.45, customer=user1)
    ORDERS_DB["o2"] = Order(id="o2", total=67.89, customer=user2)

_seed_demo_data()

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_order_by_id(order_id: str) -> Order:
    """Retrieve an order from the in‑memory DB or raise ValueError."""
    try:
        return ORDERS_DB[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' does not exist.") from exc

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

PLACEHOLDER_PATTERN = re.compile(r"\{(?P<path>[a-zA-Z_][\w\.]*)\}")

def create_user_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string by filling placeholders in the given template
    with data from the order and its customer.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        Receipt template containing placeholders such as `{customer.name}`
        or `{order.total}`.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if the customer data is restricted.
    """
    # Fetch order
    order = _get_order_by_id(order_id)

    # Security check: disallow restricted customers
    if order.customer.is_restricted:
        raise ValueError("Access to restricted customer data is not allowed.")

    # Build a context dictionary that supports dotted paths
    def resolve_path(path: str):
        parts = path.split(".")
        obj = locals()
        for part in parts:
            if isinstance(obj, dict):
                # local variables dictionary
                obj = obj.get(part)
            else:
                try:
                    obj = getattr(obj, part)
                except AttributeError as exc:
                    raise ValueError(f"Invalid placeholder path: '{path}'") from exc
        return obj

    # Replace placeholders
    def replace_match(match: re.Match) -> str:
        path = match.group("path")
        value = resolve_path(path)
        # Convert non-string values to string
        return str(value)

    receipt = PLACEHOLDER_PATTERN.sub(replace_match, template)
    return receipt

# --------------------------------------------------------------------------- #
# Example usage (for testing only – remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total:.2f}\n"
    )
    try:
        print(create_user_receipt("o1", tmpl))
        # The following will raise an error due to restricted customer
        print(create_user_receipt("o2", tmpl))
    except ValueError as e:
        print(f"Error: {e}")