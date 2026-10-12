import json
from dataclasses import dataclass, asdict
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Domain entities – normally these would be imported from the platform's
# data‑access layer.  They are simplified here for demonstration purposes.
# --------------------------------------------------------------------------- #

@dataclass
class Customer:
    id: str
    name: str
    email: str
    # The following attribute is intentionally *protected*; it should never be
    # exposed in a receipt.  Attempting to access it will raise an exception.
    _ssn: str | None = None

@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: list[Dict[str, Any]]
    # The following attribute is a sensitive internal flag that must not be
    # leaked through the receipt.
    _internal_flag: bool = False

# --------------------------------------------------------------------------- #
# Repository – a very small in‑memory implementation that mimics a real
# persistence layer.  In production code this would talk to a database.
# --------------------------------------------------------------------------- #

class OrderRepository:
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
        try:
            return cls._orders[order_id]
        except KeyError as exc:
            raise ValueError(f"Order ID '{order_id}' not found") from exc

    @classmethod
    def get_customer(cls, customer_id: str) -> Customer:
        try:
            return cls._customers[customer_id]
        except KeyError as exc:
            raise ValueError(f"Customer ID '{customer_id}' not found") from exc

# --------------------------------------------------------------------------- #
# Helper – safe dictionary that blocks access to protected attributes.
# --------------------------------------------------------------------------- #

class SafeTemplateDict(dict):
    """
    A dict wrapper that raises ValueError if a key starts with an underscore
    (i.e. attempts to access protected attributes).
    """
    def __getitem__(self, key):
        if isinstance(key, str) and key.startswith("_"):
            raise ValueError(f"Access to protected attribute '{key}' is forbidden")
        return super().__getitem__(key)

# --------------------------------------------------------------------------- #
# Main function – the requested API.
# --------------------------------------------------------------------------- #

def compose_invoice_template(invoice_id: str, receipt_format: str) -> str:
    """
    Generate a formatted receipt string for the given order ID.

    Parameters
    ----------
    invoice_id : str
        Identifier of the order.
    receipt_format : str
        Template string containing placeholders such as '{customer.name}'
        and '{order.total}'.

    Returns
    -------
    str
        The fully formatted receipt.

    Raises
    ------
    ValueError
        If the order ID is invalid or if a protected attribute is accessed.
    """
    # Retrieve the order and its customer from the repository
    order = OrderRepository.get_order(invoice_id)
    customer = OrderRepository.get_customer(order.customer_id)

    # Convert domain objects to plain dictionaries
    order_dict = asdict(order)
    customer_dict = asdict(customer)

    # Flatten nested dictionaries for simple template substitution
    flat_context: Dict[str, Any] = {}

    # Helper to flatten dict with prefix
    def _flatten(prefix: str, mapping: Dict[str, Any]) -> None:
        for k, v in mapping.items():
            if isinstance(v, dict):
                _flatten(f"{prefix}{k}.", v)
            else:
                flat_context[f"{prefix}{k}"] = v

    _flatten("order.", order_dict)
    _flatten("customer.", customer_dict)

    # Ensure protected attributes are not exposed
    for key in flat_context.keys():
        if key.startswith("order._") or key.startswith("customer._"):
            raise ValueError(f"Attempt to expose protected attribute '{key}'")

    # Perform the substitution using a safe dictionary
    template_dict = SafeTemplateDict(flat_context)
    try:
        receipt = receipt_format.format_map(template_dict)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in template: {exc}") from exc

    return receipt

# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Setup sample data
    customer = Customer(id="c123", name="Alice Smith", email="alice@example.com")
    OrderRepository.add_customer(customer)

    order = Order(
        id="o456",
        customer_id=customer.id,
        total=149.99,
        items=[{"name": "Widget", "qty": 2, "price": 49.99},
               {"name": "Gadget", "qty": 1, "price": 49.99}]
    )
    OrderRepository.add_order(order)

    # Define a receipt template
    tmpl = (
        "Invoice #{order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total:.2f}\n"
        "Items:\n"
        "{items_list}"
    )

    # Prepare a custom placeholder for items list
    def render_items(items):
        return "\n".join(f"  - {i['name']} x{i['qty']}: ${i['price']:.2f}"
                         for i in items)

    # Extend context with the rendered items list
    context = {
        "items_list": render_items(order.items)
    }

    # Render receipt
    final_receipt = tmpl.format(**context)
    print(final_receipt)