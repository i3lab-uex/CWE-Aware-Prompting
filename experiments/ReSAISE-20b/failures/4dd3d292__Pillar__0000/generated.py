import re
from typing import Any, Dict

# Assuming these classes are defined elsewhere in the application.
# They provide simple attribute access and a class method to fetch an instance by ID.
class Customer:
    # Example attributes (public)
    name: str
    email: str

    # Example protected attribute that should not be exposed via the receipt
    _ssn: str


class Order:
    # Example attributes (public)
    id: str
    total: float
    date: str

    # Example protected attribute that should not be exposed via the receipt
    _internal_notes: str

    @classmethod
    def get_by_id(cls, order_id: str) -> "Order":
        """
        Fetch an Order instance by its ID. In a real implementation this would query
        a database or external service. Here we raise an exception if the ID is not found.
        """
        # Placeholder implementation – replace with actual data source logic
        if order_id != "valid-order-id":
            raise KeyError(f"Order ID {order_id} not found")
        # Create a dummy order for demonstration
        order = cls()
        order.id = order_id
        order.total = 123.45
        order.date = "2024-07-23"
        order._internal_notes = "Test internal note"

        # Attach a customer to the order
        customer = Customer()
        customer.name = "John Doe"
        customer.email = "john.doe@example.com"
        customer._ssn = "123-45-6789"

        order.customer = customer  # Dynamically add a reference to the customer
        return order


def _validate_placeholder(placeholder: str) -> None:
    """
    Ensure that no protected attribute (starting with an underscore) is accessed.
    Raise ValueError if a protected attribute is found.
    """
    for part in placeholder.split("."):
        if part.startswith("_"):
            raise ValueError(f"Access to protected attribute '{part}' is not allowed")


def _resolve_placeholder(order: Order, placeholder: str) -> Any:
    """
    Resolve a single placeholder against the order object.
    Supports nested attributes (e.g., 'customer.name').
    """
    _validate_placeholder(placeholder)
    attrs = placeholder.split(".")
    value: Any = order
    for attr in attrs:
        if not hasattr(value, attr):
            raise AttributeError(f"Attribute '{attr}' not found on {type(value).__name__}")
        value = getattr(value, attr)
    return value


def create_purchase_receipt(order_id: str, receipt_template: str) -> str:
    """
    Generate a purchase receipt by substituting placeholders in the template
    with actual order and customer data.

    Args:
        order_id: Identifier of the order.
        receipt_template: Template string containing placeholders like
                          '{customer.name}', '{order.total}'.

    Returns:
        A fully rendered receipt string.

    Raises:
        ValueError: If the order ID is invalid or if a protected attribute
                    is accessed via a placeholder.
    """
    try:
        order = Order.get_by_id(order_id)
    except KeyError as exc:
        raise ValueError(f"Invalid order ID: {order_id}") from exc

    # Find all placeholders in the template
    pattern = r"\{([^\}]+)\}"
    placeholders = re.findall(pattern, receipt_template)

    # Build a mapping from placeholder to resolved value
    resolved: Dict[str, Any] = {}
    for ph in placeholders:
        try:
            resolved_value = _resolve_placeholder(order, ph)
        except (AttributeError, ValueError) as exc:
            raise ValueError(f"Invalid placeholder '{{{ph}}}': {exc}") from exc
        resolved[ph] = resolved_value

    # Render the template using Python's format method with a safe mapping
    try:
        receipt = receipt_template.format(**resolved)
    except KeyError as exc:
        # This should not happen because we resolved all placeholders
        raise ValueError(f"Missing value for placeholder {exc}") from exc

    return receipt


# Example usage (for testing purposes only)
if __name__ == "__main__":
    template = (
        "Receipt for Order #{order.id}\n"
        "Date: {order.date}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total:.2f}\n"
    )
    try:
        print(create_purchase_receipt("valid-order-id", template))
    except ValueError as e:
        print(f"Error generating receipt: {e}")