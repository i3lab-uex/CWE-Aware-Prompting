import re
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mock definitions for Order and Customer (in a real application these
# would be imported from the application's domain model).
# ----------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email  # Assume this field is restricted

class Order:
    _orders: Dict[str, "Order"] = {}

    def __init__(self, order_id: str, customer: Customer, total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total

    @classmethod
    def register(cls, order: "Order") -> None:
        cls._orders[order.order_id] = order

    @classmethod
    def get_by_id(cls, order_id: str) -> "Order | None":
        return cls._orders.get(order_id)


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _extract_placeholders(template: str) -> set[str]:
    """
    Extract all placeholders from a template string. Placeholders are
    expected to be in the form {key}.
    """
    return set(re.findall(r"{([^{}]+)}", template))


def _build_mapping(order: Order) -> Dict[str, Any]:
    """
    Build a mapping of placeholder keys to values from an Order instance.
    Only non‑restricted fields are exposed. Restricted fields raise
    ValueError when encountered in the template.
    """
    mapping: Dict[str, Any] = {
        "customer.name": order.customer.name,
        "order.total": f"{order.total:.2f}",
        "order.id": order.order_id,
    }
    # If you want to expose more fields, add them here carefully.
    return mapping


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_client_receipt(order_id: str, template: str) -> str:
    """
    Generate a formatted receipt string for the given order ID and
    template. The function validates the order ID, checks that no
    restricted customer data is requested in the template, and then
    substitutes placeholders with actual order/customer values.

    Raises:
        ValueError: If the order ID is invalid, or if the template
                    requests restricted data (e.g., customer.email).
    """
    # Retrieve the order. Raise if not found.
    order = Order.get_by_id(order_id)
    if order is None:
        raise ValueError(f"Invalid order ID: {order_id}")

    # Identify placeholders in the template.
    placeholders = _extract_placeholders(template)

    # Check for restricted data access.
    if any(ph.startswith("customer.email") for ph in placeholders):
        raise ValueError("Attempt to access restricted customer data")

    # Build mapping for allowed placeholders.
    mapping = _build_mapping(order)

    # Ensure all placeholders are supported; otherwise raise an error.
    unsupported = placeholders - set(mapping.keys())
    if unsupported:
        raise ValueError(f"Unsupported placeholder(s) in template: {', '.join(sorted(unsupported))}")

    # Perform substitution. Use a safe format method to avoid KeyError.
    try:
        receipt = template.format(**mapping)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Error formatting receipt: {exc}") from exc

    return receipt


# ----------------------------------------------------------------------
# Example usage (this part would normally be outside this module)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Setup mock data
    cust = Customer(name="Alice Smith", email="alice@example.com")
    order = Order(order_id="ORD12345", customer=cust, total=149.99)
    Order.register(order)

    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name}\n"
        "Total: ${order.total}"
    )
    print(generate_client_receipt("ORD12345", tmpl))