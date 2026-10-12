import re
from typing import Dict, Any

# ------------------------------------------------------------------
# Dummy data models (in a real application these would come from
# the e‑commerce system's ORM or service layer).
# ------------------------------------------------------------------

class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email  # Sensitive field – should not be exposed

class Order:
    def __init__(self, order_id: str, total: float, customer: User):
        self.order_id = order_id
        self.total = total
        self.customer = customer

# A very small in‑memory "database" for demo purposes.
ORDERS_DB: Dict[str, Order] = {}

def _register_demo_orders():
    """Populate the demo database with a few orders."""
    customer1 = User(name="Alice Smith", email="alice@example.com")
    customer2 = User(name="Bob Jones", email="bob@example.com")

    ORDERS_DB["ORD001"] = Order(order_id="ORD001", total=149.99, customer=customer1)
    ORDERS_DB["ORD002"] = Order(order_id="ORD002", total=79.50, customer=customer2)

_register_demo_orders()


# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def _get_order(order_id: str) -> Order:
    """Retrieve an order by its ID, raising ValueError if not found."""
    try:
        return ORDERS_DB[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' is invalid.") from exc


def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    return set(re.findall(r"{([^{}]+)}", template))


def _build_context(order: Order) -> Dict[str, Any]:
    """
    Build a context dictionary for formatting the template.
    Only expose whitelisted fields. Any attempt to access
    restricted data will raise ValueError.
    """
    context: Dict[str, Any] = {}

    # Expose customer data
    if hasattr(order.customer, "name"):
        context["customer.name"] = order.customer.name
    else:
        raise ValueError("Customer data is missing required 'name' field.")

    # Expose order data
    if hasattr(order, "total"):
        context["order.total"] = f"{order.total:.2f}"
    else:
        raise ValueError("Order data is missing required 'total' field.")

    return context


def _validate_placeholders(placeholders: set[str], context_keys: set[str]) -> None:
    """
    Ensure that every placeholder in the template can be satisfied by
    the context. Raise ValueError if any unsupported placeholder is found.
    """
    for key in placeholders:
        if key not in context_keys:
            raise ValueError(f"Unsupported placeholder '{{{key}}}' in template.")


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def create_user_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order ID using the supplied
    template. The template may contain placeholders such as
    '{customer.name}' and '{order.total}'. Only these fields are allowed;
    any attempt to access other data will result in a ValueError.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        Receipt pattern containing placeholders.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if the template contains an
        unsupported placeholder.
    """
    # 1. Retrieve order, raising ValueError if not found
    order = _get_order(order_id)

    # 2. Extract placeholders from template
    placeholders = _extract_placeholders(template)

    # 3. Build context dictionary for allowed fields
    context = _build_context(order)

    # 4. Validate that all placeholders are supported
    _validate_placeholders(placeholders, set(context.keys()))

    # 5. Perform formatting
    try:
        receipt = template.format(**context)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return receipt


# ------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# ------------------------------------------------------------------

# if __name__ == "__main__":
#     tmpl = (
#         "Dear {customer.name},\n"
#         "Thank you for your purchase!\n"
#         "Order Total: ${order.total}\n"
#         "Your order ID is {order_id}."
#     )
#     # Note: 'order_id' placeholder isn't part of our whitelist, so we
#     # should handle it manually or remove it from the template.
#     receipt = create_user_receipt("ORD001", tmpl.replace("{order_id}", "ORD001"))
#     print(receipt)