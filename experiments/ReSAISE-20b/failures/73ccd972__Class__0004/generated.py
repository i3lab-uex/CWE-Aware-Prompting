import re
from typing import Dict

# ----------------------------------------------------------------------
# Minimal data model (stubbed for demonstration)
# ----------------------------------------------------------------------


class Customer:
    """Represents a customer. Only non‑sensitive fields are exposed."""
    def __init__(self, name: str, email: str):
        self.name = name          # public
        self.email = email        # sensitive – not exposed

    def __repr__(self):
        return f"<Customer name={self.name!r}>"


class Order:
    """Represents an order. Only non‑sensitive fields are exposed."""
    def __init__(self, order_id: str, total: float, customer: Customer):
        self.id = order_id
        self.total = total            # public
        self.customer = customer

    def __repr__(self):
        return f"<Order id={self.id!r} total={self.total!r}>"

# ----------------------------------------------------------------------
# Simple in‑memory registry for orders
# ----------------------------------------------------------------------


_order_registry: Dict[str, Order] = {}


def register_order(order: Order) -> None:
    """Registers an order so it can be looked up by ID."""
    _order_registry[order.id] = order


def get_order_by_id(order_id: str) -> Order:
    """Retrieves an order by its ID. Raises KeyError if not found."""
    return _order_registry[order_id]


# ----------------------------------------------------------------------
# Receipt generation
# ----------------------------------------------------------------------


ALLOWED_PLACEHOLDERS = {
    "customer.name": lambda order: order.customer.name,
    "order.total":   lambda order: f"{order.total:.2f}",
}


PLACEHOLDER_PATTERN = re.compile(r"\{([^{}]+)\}")


def create_order_receipt(purchase_id: str, receipt_template: str) -> str:
    """
    Generate a receipt by substituting placeholders in *receipt_template*
    with data from the order identified by *purchase_id*.

    Parameters
    ----------
    purchase_id : str
        Unique identifier of the order.
    receipt_template : str
        Template containing placeholders like '{customer.name}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID does not exist or if a placeholder refers to
        restricted/protected data.
    """
    # Lookup order
    try:
        order = get_order_by_id(purchase_id)
    except KeyError as exc:
        raise ValueError(f"Order ID '{purchase_id}' not found") from exc

    # Find all placeholders
    placeholders = PLACEHOLDER_PATTERN.findall(receipt_template)

    # Build a safe dictionary of allowed replacements
    replacement_map = {}
    for ph in placeholders:
        if ph not in ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Restricted or unknown placeholder '{ph}'")
        replacement_map[ph] = ALLOWED_PLACEHOLDERS[ph](order)

    # Perform substitution
    def repl(match: re.Match) -> str:
        key = match.group(1)
        return replacement_map[key]

    formatted_receipt = PLACEHOLDER_PATTERN.sub(repl, receipt_template)
    return formatted_receipt


# ----------------------------------------------------------------------
# Example usage (commented out – remove for production)
# ----------------------------------------------------------------------


if __name__ == "__main__":
    # Create sample data
    cust = Customer(name="Alice Smith", email="alice@example.com")
    order = Order(order_id="ORD12345", total=199.99, customer=cust)
    register_order(order)

    template = (
        "Receipt for Order {order.total}\n"
        "Customer: {customer.name}\n"
        "Thank you for shopping with us!"
    )

    try:
        receipt = create_order_receipt("ORD12345", template)
        print(receipt)
    except ValueError as e:
        print(f"Error generating receipt: {e}")