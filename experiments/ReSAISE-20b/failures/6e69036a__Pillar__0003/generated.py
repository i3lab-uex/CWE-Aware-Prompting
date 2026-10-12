import re
from typing import Any, Dict

# Mocked data layer (replace with real implementations)
class Customer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email  # Assume this field is restricted


class Order:
    _orders_db: Dict[str, "Order"] = {}

    def __init__(self, order_id: str, customer: Customer, total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total

    @classmethod
    def get_by_id(cls, order_id: str) -> "Order":
        """
        Retrieve an Order instance by its ID.
        Raises ValueError if the order does not exist.
        """
        try:
            return cls._orders_db[order_id]
        except KeyError as exc:
            raise ValueError(f"Order ID '{order_id}' not found") from exc

    @classmethod
    def _register(cls, order: "Order"):
        cls._orders_db[order.order_id] = order


# Example data registration (for illustration only)
_customer = Customer(name="Alice Smith", email="alice@example.com")
_order_example = Order(order_id="12345", customer=_customer, total=99.95)
Order._register(_order_example)


def _get_attr_by_path(obj: Any, path: str) -> Any:
    """
    Safely retrieve nested attributes from an object using a dotted path.
    Raises AttributeError if any part of the path is invalid.
    """
    for attr in path.split("."):
        obj = getattr(obj, attr)
    return obj


def generate_client_receipt(order_id: str, template: str) -> str:
    """
    Generate a formatted receipt string for the given order ID using the supplied template.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A format string containing placeholders such as '{customer.name}' or '{order.total}'.

    Returns
    -------
    str
        The receipt with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the order ID is invalid or if a restricted data field is requested.
    """
    # Fetch the order; this may raise ValueError if ID is invalid
    order = Order.get_by_id(order_id)

    # Restricted fields that should not be exposed in the receipt
    restricted_fields = {"customer.email"}

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"{([^{}]+)}")
    placeholders = placeholder_pattern.findall(template)

    # Prepare a mapping for formatting
    format_mapping: Dict[str, Any] = {}

    for placeholder in placeholders:
        # Check for restricted data
        if placeholder.strip() in restricted_fields:
            raise ValueError(f"Attempt to access restricted data: '{placeholder}'")

        # Resolve the value
        try:
            if placeholder.startswith("order."):
                value = _get_attr_by_path(order, placeholder[len("order.") :])
            elif placeholder.startswith("customer."):
                value = _get_attr_by_path(order.customer, placeholder[len("customer.") :])
            else:
                raise ValueError(f"Unknown placeholder prefix in '{placeholder}'")
        except AttributeError as exc:
            raise ValueError(f"Invalid placeholder '{placeholder}': {exc}") from exc

        format_mapping[placeholder] = value

    # Perform the formatting
    try:
        receipt = template.format(**format_mapping)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return receipt