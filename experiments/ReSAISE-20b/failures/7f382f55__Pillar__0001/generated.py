import json
from dataclasses import dataclass, field
from typing import Dict, Any

# ------------------------------------------------------------------
# Mocked data store (in a real system this would be a database or API)
# ------------------------------------------------------------------
ORDER_DB: Dict[str, "Order"] = {}
CUSTOMER_DB: Dict[int, "Customer"] = {}


# ------------------------------------------------------------------
# Domain models
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Customer:
    id: int
    name: str
    email: str
    _ssn: str = field(repr=False)  # protected attribute, should not be exposed

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation excluding protected fields."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }


@dataclass(frozen=True)
class Order:
    id: str
    customer_id: int
    total: float
    items: list

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the order."""
        customer = CUSTOMER_DB.get(self.customer_id)
        if not customer:
            raise ValueError(f"Customer with id {self.customer_id} not found")
        return {
            "id": self.id,
            "customer": customer.to_dict(),
            "total": self.total,
            "items": self.items
        }


# ------------------------------------------------------------------
# Helper functions for loading resources safely
# ------------------------------------------------------------------
def load_order(order_id: str) -> Order:
    """Load an order by ID, raising ValueError if not found."""
    order = ORDER_DB.get(order_id)
    if not order:
        raise ValueError(f"Invalid order ID: {order_id}")
    return order


# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------
def compose_invoice_template(invoice_id: str, receipt_format: str) -> str:
    """
    Generate a formatted receipt for the given order ID.

    Parameters
    ----------
    invoice_id : str
        The identifier of the order.
    receipt_format : str
        A template string containing placeholders, e.g.
        '{customer.name}', '{order.total}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if protected customer data is accessed.
    """
    # Load the order (resource acquisition)
    order = load_order(invoice_id)

    # Build a context dictionary with safe keys only
    context: Dict[str, Any] = {}
    order_dict = order.to_dict()
    customer_dict = order_dict["customer"]

    # Expose only non‑protected fields
    context["order"] = {
        "id": order_dict["id"],
        "total": order_dict["total"],
        "items": order_dict["items"]
    }
    context["customer"] = customer_dict

    # Prevent accidental access to protected fields
    for key in receipt_format.split("{")[1:]:
        placeholder = key.split("}")[0]
        if "_" in placeholder.split(".")[-1]:
            raise ValueError(f"Access to protected field '{placeholder}' is not allowed")

    # Perform safe formatting
    try:
        receipt = receipt_format.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in template: {exc}") from None

    return receipt


# ------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Populate mock databases
    CUSTOMER_DB[1] = Customer(id=1, name="Alice", email="alice@example.com", _ssn="123-45-6789")
    ORDER_DB["ORD001"] = Order(
        id="ORD001",
        customer_id=1,
        total=99.99,
        items=[{"name": "Widget", "price": 49.99}, {"name": "Gadget", "price": 50.00}]
    )

    template = (
        "Invoice #{order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total}\n"
        "Items:\n{order.items}"
    )

    print(compose_invoice_template("ORD001", template))