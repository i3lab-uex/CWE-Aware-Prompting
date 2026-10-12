import re
from typing import Any, Dict

# Assume these classes are provided by the platform.
class Customer:
    def __init__(self, name: str, email: str, _ssn: str = None):
        self.name = name
        self.email = email
        # protected attribute (should not be exposed)
        if _ssn:
            self._ssn = _ssn

class Order:
    def __init__(self, order_id: str, customer: Customer,
                 total: float, items: list):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items

# Mock database of orders (in a real system this would be a DB query)
ORDER_DB: Dict[str, Order] = {}

def get_order_by_id(order_id: str) -> Order:
    """Retrieve an order by its ID from the mock database."""
    if not isinstance(order_id, str) or not order_id:
        raise ValueError("Order ID must be a non-empty string.")
    try:
        return ORDER_DB[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' not found.") from exc

def _extract_placeholders(template: str) -> set[str]:
    """
    Extract all unique placeholders from the template.
    Placeholders are of the form {field} or {object.field}.
    """
    pattern = re.compile(r"{([a-zA-Z_][\w\.]*)}")
    return set(pattern.findall(template))

def _build_context(order: Order) -> Dict[str, Any]:
    """
    Build a dictionary of values that can be safely injected into the template.
    Only allows public attributes (no leading underscore) of order and customer.
    """
    context = {}
    # Order-level attributes
    for attr in dir(order):
        if attr.startswith("_"):
            continue
        val = getattr(order, attr)
        if not callable(val):
            context[attr] = val

    # Customer-level attributes
    customer = getattr(order, "customer", None)
    if customer:
        for attr in dir(customer):
            if attr.startswith("_"):
                continue
            val = getattr(customer, attr)
            if not callable(val):
                # Prefix with 'customer.' to avoid clashes
                context[f"customer.{attr}"] = val

    return context

def create_purchase_receipt(order_id: str, receipt_template: str) -> str:
    """
    Generate a receipt string by filling in placeholders in the template
    with data from the specified order.

    Parameters:
        order_id (str): Identifier of the order.
        receipt_template (str): Template containing placeholders like
                                '{customer.name}', '{order.total}'.

    Returns:
        str: The formatted receipt.

    Raises:
        ValueError: If the order ID is invalid, if protected data is requested,
                    or if placeholders cannot be resolved.
    """
    # Validate template
    if not isinstance(receipt_template, str):
        raise ValueError("Receipt template must be a string.")

    # Retrieve order
    order = get_order_by_id(order_id)

    # Build safe context for formatting
    context = _build_context(order)

    # Validate that all placeholders are resolvable and not protected
    placeholders = _extract_placeholders(receipt_template)
    for key in placeholders:
        if key not in context:
            # Check if it refers to a protected attribute
            parts = key.split(".")
            obj_name, attr = (parts[0], parts[1]) if len(parts) == 2 else ("order", key)
            if obj_name == "customer":
                customer = order.customer
                if hasattr(customer, f"_{attr}") or attr.startswith("_"):
                    raise ValueError(f"Attempt to access protected customer attribute '{attr}'.")
            elif obj_name == "order":
                if hasattr(order, f"_{attr}") or attr.startswith("_"):
                    raise ValueError(f"Attempt to access protected order attribute '{attr}'.")
            else:
                raise ValueError(f"Unknown placeholder '{{{key}}}' in template.")
    # Format the receipt
    try:
        receipt = receipt_template.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from exc
    return receipt

# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate mock database
    cust = Customer(name="Alice Smith", email="alice@example.com")
    ORDER_DB["ORD123"] = Order(
        order_id="ORD123",
        customer=cust,
        total=149.99,
        items=[{"name": "T-shirt", "qty": 2, "price": 29.99},
               {"name": "Jeans", "qty": 1, "price": 89.99}]
    )

    template = (
        "Thank you for your purchase, {customer.name}!\n"
        "Order ID: {order_id}\n"
        "Total: ${total:.2f}\n"
        "Items:\n{items}"
    )
    # Convert items list to string
    order = ORDER_DB["ORD123"]
    items_str = "\n".join(f"  - {item['name']} x{item['qty']}: ${item['price']:.2f}"
                          for item in order.items)
    # Replace placeholder {items} manually (since list cannot be formatted directly)
    final_template = template.replace("{items}", items_str)

    print(create_purchase_receipt("ORD123", final_template))