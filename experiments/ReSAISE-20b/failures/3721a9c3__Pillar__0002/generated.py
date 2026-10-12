import re
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Assume these classes and helper functions are provided by the application.
# They are included here only as minimal stubs for demonstration purposes.
# --------------------------------------------------------------------------- #

class Customer:
    def __init__(self, name: str, email: str, ssn: str):
        self.name = name
        self.email = email
        self.ssn = ssn  # Sensitive data that must not be exposed

class Order:
    def __init__(self, order_id: str, customer: Customer, total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total

# In a real application this would query a database or an external service.
def _get_order_by_id(order_id: str) -> Order:
    # Dummy implementation for illustration.
    if order_id == "invalid":
        raise KeyError("Order not found")
    cust = Customer(name="John Doe", email="john@example.com", ssn="123-45-6789")
    return Order(order_id=order_id, customer=cust, total=99.95)

# --------------------------------------------------------------------------- #
# The actual implementation of generate_buyer_receipt
# --------------------------------------------------------------------------- #

def _extract_placeholders(template: str) -> set:
    """
    Extracts all placeholders in the form {field} from the template.
    Returns a set of placeholder names.
    """
    # Simple regex to capture words inside braces
    return set(re.findall(r"{([a-zA-Z0-9_.]+)}", template))

def _build_context(order: Order) -> Dict[str, Any]:
    """
    Builds a safe dictionary of values that can be used to format the template.
    Only non-sensitive attributes are exposed.
    """
    context = {
        "customer.name": order.customer.name,
        "order.total": f"{order.total:.2f}",
    }
    return context

def generate_buyer_receipt(order_id: str, template: str) -> str:
    """
    Generates a buyer receipt by filling in the provided template with
    data from the order identified by `order_id`.

    Parameters:
        order_id (str): Unique identifier for the order.
        template (str): Template string containing placeholders such as
                        '{customer.name}' and '{order.total}'.

    Returns:
        str: The formatted receipt string.

    Raises:
        ValueError: If the order ID is invalid, if restricted data is
                    requested via placeholders, or if placeholder names are
                    unknown.
    """
    # 1. Retrieve the order; raise ValueError if not found
    try:
        order = _get_order_by_id(order_id)
    except KeyError as exc:
        raise ValueError(f"Invalid order ID: {order_id}") from exc

    # 2. Validate placeholders
    allowed_placeholders = {"customer.name", "order.total"}
    found_placeholders = _extract_placeholders(template)

    # Check for restricted data
    if "customer.ssn" in found_placeholders:
        raise ValueError("Attempt to access restricted customer data")

    # Ensure all placeholders are known
    unknown = found_placeholders - allowed_placeholders
    if unknown:
        raise ValueError(f"Unknown placeholders in template: {', '.join(sorted(unknown))}")

    # 3. Build context and perform formatting
    context = _build_context(order)

    try:
        receipt = template.format(**context)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return receipt

# --------------------------------------------------------------------------- #
# Example usage (for local testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = "Dear {customer.name},\nYour order total is ${order.total}."
    print(generate_buyer_receipt("12345", tmpl))