import re
from typing import Any, Dict

# --------------------------------------------------------------------------- #
#   Dummy data models (replace with real implementations in the application)
# --------------------------------------------------------------------------- #

class Customer:
    """Represents a customer."""
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email  # considered restricted


class Order:
    """Represents an order."""
    _orders: Dict[str, "Order"] = {}

    def __init__(self, order_id: str, total: float, customer: Customer):
        self.order_id = order_id
        self.total = total
        self.customer = customer

    @classmethod
    def get_by_id(cls, order_id: str) -> "Order":
        """Retrieve an Order by its ID. Raises KeyError if not found."""
        try:
            return cls._orders[order_id]
        except KeyError as exc:
            raise KeyError(f"Order ID {order_id!r} not found") from exc

    @classmethod
    def register(cls, order: "Order"):
        """Register an Order for retrieval."""
        cls._orders[order.order_id] = order


# --------------------------------------------------------------------------- #
#   Core function
# --------------------------------------------------------------------------- #

def generate_buyer_receipt(order_id: str, template: str) -> str:
    """
    Generate a formatted receipt for the buyer.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A format string containing placeholders such as '{customer.name}' or
        '{order.total}'.  The function will replace these placeholders with the
        corresponding data.

    Returns
    -------
    str
        The receipt string with all placeholders substituted.

    Raises
    ------
    ValueError
        If the order ID is invalid or if a restricted customer attribute is
        referenced in the template.
    """
    # Validate order ID and fetch the order object
    try:
        order = Order.get_by_id(order_id)
    except KeyError as exc:
        raise ValueError(f"Invalid order ID: {order_id}") from exc

    # Define which attributes are allowed to be exposed
    ALLOWED_CUSTOMER_ATTRS = {"name"}
    # Use regex to find all placeholders in the template
    placeholder_pattern = re.compile(r"{([^{}]+)}")
    placeholders = placeholder_pattern.findall(template)

    # Build a context dictionary for str.format()
    context: Dict[str, Any] = {}

    for placeholder in placeholders:
        # Split on '.' to navigate nested attributes
        parts = placeholder.split(".")
        if not parts:
            continue

        # Resolve the root object (either 'order' or 'customer')
        root_name = parts[0]
        if root_name == "order":
            obj: Any = order
        elif root_name == "customer":
            obj = order.customer
        else:
            raise ValueError(f"Unsupported placeholder root: {root_name}")

        # Resolve subsequent attributes
        for attr in parts[1:]:
            if not hasattr(obj, attr):
                raise ValueError(f"Attribute {attr!r} does not exist on {obj.__class__.__name__}")
            if root_name == "customer" and attr not in ALLOWED_CUSTOMER_ATTRS:
                raise ValueError(f"Access to restricted customer attribute '{attr}' is not allowed")
            obj = getattr(obj, attr)

        # Store the resolved value in context
        context[placeholder] = obj

    try:
        receipt = template.format(**context)
    except KeyError as exc:
        # This should not happen because we resolved all placeholders
        raise ValueError(f"Missing placeholder data for {exc}") from exc

    return receipt


# --------------------------------------------------------------------------- #
#   Example usage (for demonstration only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Create a customer and an order
    cust = Customer(name="Alice Smith", email="alice@example.com")
    ord_ = Order(order_id="ORD123", total=199.99, customer=cust)
    Order.register(ord_)

    # Define a receipt template
    tmpl = (
        "Receipt for {customer.name}\n"
        "Order ID: {order.order_id}\n"
        "Total Amount: ${order.total:.2f}"
    )

    # Generate receipt
    print(generate_buyer_receipt("ORD123", tmpl))