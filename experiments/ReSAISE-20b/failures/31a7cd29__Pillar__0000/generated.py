import re
from typing import Dict

# ----------------------------------------------------------------------
# Mock data store and entity definitions (for demonstration purposes)
# In a real application these would be replaced by ORM models or
# service‑layer calls that fetch data from a database.
# ----------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str, address: str, ssn: str):
        self.name = name
        self.email = email
        self.address = address
        self.ssn = ssn  # protected field


class Order:
    def __init__(self, order_id: str, total: float, items: list, customer: Customer):
        self.id = order_id
        self.total = total
        self.items = items
        self.customer = customer


# Simple in‑memory registry of orders for demo purposes.
ORDER_REGISTRY: Dict[str, Order] = {}


# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
def _get_order(order_identifier: str) -> Order:
    """Retrieve an order by its identifier from the registry."""
    try:
        return ORDER_REGISTRY[order_identifier]
    except KeyError as exc:
        raise ValueError(f"Order with id '{order_identifier}' does not exist.") from exc


def _extract_placeholders(template: str) -> set:
    """Return a set of all placeholders found in the template string."""
    # Use regex to find {field} patterns
    return set(re.findall(r"{([^{}]+)}", template))


def _build_mapping(order: Order) -> Dict[str, str]:
    """
    Build a mapping dictionary for allowed placeholders.

    The keys are the placeholder names (e.g., 'customer.name')
    and the values are the string representations of the corresponding attributes.
    """
    mapping: Dict[str, str] = {}

    # Customer attributes
    customer_attrs = {
        "name": order.customer.name,
        "email": order.customer.email,
        "address": order.customer.address,
    }

    # Order attributes
    order_attrs = {
        "id": order.id,
        "total": f"{order.total:.2f}",
        "items": ", ".join(order.items),
    }

    # Populate mapping
    for key, value in customer_attrs.items():
        mapping[f"customer.{key}"] = str(value)
    for key, value in order_attrs.items():
        mapping[f"order.{key}"] = str(value)

    return mapping


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_order_receipt(order_identifier: str, template_string: str) -> str:
    """
    Generate a formatted receipt for the given order.

    Args:
        order_identifier: The unique identifier of the order.
        template_string: A string containing placeholders like
                         '{customer.name}', '{order.total}', etc.

    Returns:
        A fully formatted receipt string with placeholders replaced by
        actual order and customer data.

    Raises:
        ValueError: If the order does not exist or if a placeholder
                    requests restricted data.
    """
    # Retrieve order (raises ValueError if not found)
    order = _get_order(order_identifier)

    # Extract placeholders from template
    placeholders = _extract_placeholders(template_string)

    # Define allowed placeholder namespaces and attributes
    allowed_customer_attrs = {"name", "email", "address"}
    allowed_order_attrs = {"id", "total", "items"}

    # Validate each placeholder
    for ph in placeholders:
        if "." not in ph:
            raise ValueError(f"Invalid placeholder format: '{ph}'. Expected 'entity.attribute'.")
        entity, attr = ph.split(".", 1)
        if entity == "customer":
            if attr not in allowed_customer_attrs:
                raise ValueError(f"Access to restricted customer attribute '{attr}' is not permitted.")
        elif entity == "order":
            if attr not in allowed_order_attrs:
                raise ValueError(f"Unknown order attribute '{attr}'.")
        else:
            raise ValueError(f"Unsupported placeholder entity '{entity}' in '{ph}'.")

    # Build mapping for allowed placeholders
    mapping = _build_mapping(order)

    # Perform safe formatting
    try:
        receipt = template_string.format(**mapping)
    except KeyError as exc:
        # This should not happen because we validated placeholders
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return receipt


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     # Create sample data
#     cust = Customer(name="Alice Smith", email="alice@example.com",
#                     address="123 Maple St, Springfield", ssn="123-45-6789")
#     ord_obj = Order(order_id="ORD001", total=150.75,
#                     items=["Widget A", "Widget B"], customer=cust)
#     ORDER_REGISTRY[ord_obj.id] = ord_obj
#
#     tmpl = (
#         "Receipt for Order {order.id}\n"
#         "Customer: {customer.name} ({customer.email})\n"
#         "Address: {customer.address}\n"
#         "Items: {order.items}\n"
#         "Total Due: ${order.total}"
#     )
#
#     print(build_order_receipt("ORD001", tmpl))