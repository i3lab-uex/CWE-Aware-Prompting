import re
from typing import Dict

# Assume these classes are provided by the platform.
class Customer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email  # Sensitive

class Order:
    _orders: Dict[str, "Order"] = {}

    def __init__(self, order_id: str, total: float, customer: Customer):
        self.id = order_id
        self.total = total
        self.customer = customer
        Order._orders[order_id] = self

    @classmethod
    def get_by_id(cls, order_id: str) -> "Order | None":
        return cls._orders.get(order_id)


def build_order_receipt(order_identifier: str, template_string: str) -> str:
    """
    Build a receipt string for the given order by replacing placeholders
    in the template with actual data.

    Allowed placeholders:
        {order.id}
        {order.total}
        {customer.name}

    Any other placeholder will raise a ValueError.
    """
    # Retrieve the order
    order = Order.get_by_id(order_identifier)
    if not order:
        raise ValueError(f"Order ID '{order_identifier}' does not exist.")

    # Mapping of allowed placeholders to their values
    placeholder_map: Dict[str, str] = {
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "customer.name": order.customer.name,
    }

    # Regex to find placeholders of the form {something}
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")

    def replace_placeholder(match: re.Match) -> str:
        key = match.group(1)
        if key not in placeholder_map:
            raise ValueError(f"Unauthorized or unknown placeholder: '{{{key}}}'")
        return placeholder_map[key]

    try:
        result = placeholder_pattern.sub(replace_placeholder, template_string)
    except ValueError as e:
        # Re‑raise to signal caller
        raise

    return result