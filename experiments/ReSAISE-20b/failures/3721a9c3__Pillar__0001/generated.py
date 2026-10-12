import re
from contextlib import contextmanager

# --------------------------------------------------------------------
# Mock data layer – in a real system this would be replaced by a database
# --------------------------------------------------------------------
class Customer:
    def __init__(self, customer_id: str, name: str, email: str, is_restricted: bool = False):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.is_restricted = is_restricted  # If True, sensitive data cannot be exposed


class Order:
    def __init__(self, order_id: str, customer: Customer, total: float, items: list):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items


# In‑memory “database” of orders
ORDERS_DB = {}


def add_order(order: Order) -> None:
    """Utility to populate the mock database."""
    ORDERS_DB[order.order_id] = order


# --------------------------------------------------------------------
# Resource handling
# --------------------------------------------------------------------
@contextmanager
def get_order(order_id: str) -> Order:
    """
    Context manager that retrieves an order from the database.
    Ensures that any required cleanup (e.g., closing DB connections)
    would happen here. For this mock, we simply yield the order.
    """
    try:
        order = ORDERS_DB[order_id]
        yield order
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' is invalid") from exc
    finally:
        # In a real scenario, we would close database connections or release locks here.
        pass


# --------------------------------------------------------------------
# Receipt generation
# --------------------------------------------------------------------
PLACEHOLDER_PATTERN = re.compile(r"\{([^{}]+)\}")


def generate_buyer_receipt(order_id: str, template: str) -> str:
    """
    Generates a receipt string for the given order ID and template.

    Parameters
    ----------
    order_id : str
        Unique identifier for the order.
    template : str
        Template containing placeholders like '{customer.name}' or '{order.total}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if restricted customer data is accessed.
    """
    with get_order(order_id) as order:
        # Build a context dictionary for string formatting
        context = {
            "customer.name": order.customer.name,
            "customer.email": order.customer.email,
            "order.total": f"{order.total:.2f}",
            "order.items": ", ".join(order.items),
        }

        # Enforce access restrictions
        if order.customer.is_restricted:
            restricted_fields = {"customer.email"}
            for field in restricted_fields:
                if f"{{{field}}}" in template:
                    raise ValueError(f"Access to restricted customer data '{field}' is prohibited")

        # Validate placeholders
        for match in PLACEHOLDER_PATTERN.finditer(template):
            placeholder = match.group(1)
            if placeholder not in context:
                raise ValueError(f"Unknown placeholder '{placeholder}' in template")

        try:
            receipt = template.format(**context)
        except KeyError as exc:
            # Should not happen due to earlier validation, but guard anyway
            raise ValueError(f"Missing data for placeholder {exc}") from exc

        return receipt


# --------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------
if __name__ == "__main__":
    # Setup mock data
    cust = Customer(customer_id="c001", name="Alice Smith", email="alice@example.com")
    order = Order(order_id="o123", customer=cust, total=149.99, items=["Widget A", "Gadget B"])
    add_order(order)

    tmpl = (
        "Receipt for {customer.name}\n"
        "Order ID: o123\n"
        "Items: {order.items}\n"
        "Total: ${order.total}"
    )
    print(generate_buyer_receipt("o123", tmpl))