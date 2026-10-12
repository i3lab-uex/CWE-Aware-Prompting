import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------------- #
# Mocked data structures – in a real application these would come from the
# database or an ORM layer.
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class User:
    id: str
    name: str
    email: str  # This field is considered restricted for receipt generation


@dataclass(frozen=True)
class Order:
    id: str
    total: float
    customer: User


# In-memory registry used only for demonstration purposes.
ORDER_REGISTRY: Dict[str, Order] = {}


def register_order(order: Order) -> None:
    """Register an order in the in-memory registry."""
    ORDER_REGISTRY[order.id] = order


def get_order_by_id(order_id: str) -> Order:
    """Retrieve an Order by its ID, raising ValueError if not found."""
    order = ORDER_REGISTRY.get(order_id)
    if order is None:
        raise ValueError(f"Order with ID '{order_id}' does not exist.")
    return order


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

RESTRICTED_FIELDS = {"customer.email", "order.id"}  # add more as needed


def _detect_restricted_placeholders(template: str) -> None:
    """
    Inspect the template for placeholders that are not allowed.
    Raises ValueError if any restricted placeholder is found.
    """
    # Find all placeholders like {something.something}
    placeholders = re.findall(r"{([^{}]+)}", template)
    for placeholder in placeholders:
        if placeholder in RESTRICTED_FIELDS:
            raise ValueError(f"Restricted data access attempted: '{{{placeholder}}}'.")


def create_user_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string by filling in the provided template with
    order and customer data.

    Parameters:
        order_id (str): The unique identifier of the order.
        template (str): A string containing placeholders such as
                        '{customer.name}' and '{order.total}'.

    Returns:
        str: The formatted receipt string.

    Raises:
        ValueError: If the order ID is invalid or if restricted customer data
                    is accessed via the template.
    """
    # Validate and fetch the order
    order = get_order_by_id(order_id)

    # Ensure no restricted data is requested
    _detect_restricted_placeholders(template)

    # Prepare mapping for format() – the placeholders are of the form
    # {customer.<attr>} and {order.<attr>}
    context = {
        "customer": order.customer,
        "order": order,
    }

    try:
        receipt = template.format(**context)
    except KeyError as exc:
        # If a placeholder refers to an attribute that doesn't exist
        raise ValueError(f"Invalid placeholder in template: {exc}") from exc

    return receipt


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to run)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     # Create sample data
#     user = User(id="u123", name="Alice Smith", email="alice@example.com")
#     order = Order(id="o456", total=99.95, customer=user)
#     register_order(order)

#     tmpl = (
#         "Receipt for Order #{order.id}\n"
#         "Customer: {customer.name}\n"
#         "Total: ${order.total:.2f}"
#     )
#     print(create_user_receipt("o456", tmpl))