import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Dummy in‑memory data store (would normally be a database)
# ----------------------------------------------------------------------
ORDERS_DB: Dict[str, "Order"] = {}
CUSTOMERS_DB: Dict[str, "Customer"] = {}

# ----------------------------------------------------------------------
# Domain classes
# ----------------------------------------------------------------------
@dataclass
class Customer:
    """Represents a customer."""
    id: str
    name: str
    email: str
    # Protected attribute – should not be exposed in a receipt.
    _ssn: str = field(repr=False, default="")

@dataclass
class Order:
    """Represents an order."""
    id: str
    customer_id: str
    total: float
    items: list[str]

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_order(order_id: str) -> Order:
    """Retrieve an order from the data store, raising ValueError if not found."""
    try:
        return ORDERS_DB[order_id]
    except KeyError as exc:
        raise ValueError(f"Invalid order ID: {order_id}") from exc

def _get_customer(customer_id: str) -> Customer:
    """Retrieve a customer from the data store, raising ValueError if not found."""
    try:
        return CUSTOMERS_DB[customer_id]
    except KeyError as exc:
        raise ValueError(f"Invalid customer ID: {customer_id}") from exc

def _safe_getattr(obj, attr_name):
    """Return attribute value if it is public; otherwise raise ValueError."""
    if attr_name.startswith("_"):
        raise ValueError(f"Attempt to access protected attribute '{attr_name}'")
    return getattr(obj, attr_name)

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def compose_invoice_template(invoice_id: str, receipt_format: str) -> str:
    """
    Generate a formatted receipt string for the given order ID.

    Parameters
    ----------
    invoice_id : str
        The identifier of the order.
    receipt_format : str
        A template string containing placeholders like '{customer.name}' or
        '{order.total}'. Placeholders may refer to nested attributes (e.g.,
        'customer.email').

    Returns
    -------
    str
        The fully rendered receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or a protected attribute is referenced.
    """
    # Retrieve the order and customer objects
    order = _get_order(invoice_id)
    customer = _get_customer(order.customer_id)

    # Regex to find placeholders like {customer.name} or {order.total}
    placeholder_pattern = re.compile(r"\{([a-zA-Z_][\w\.]*)\}")

    def replace_placeholder(match):
        full_path = match.group(1)  # e.g. 'customer.name'
        parts = full_path.split(".")
        if not parts:
            return match.group(0)

        # Resolve the root object
        root_name = parts[0]
        if root_name == "customer":
            current_obj = customer
        elif root_name == "order":
            current_obj = order
        else:
            # Unknown placeholder root – keep it unchanged
            return match.group(0)

        # Resolve nested attributes safely
        for attr in parts[1:]:
            try:
                current_obj = _safe_getattr(current_obj, attr)
            except AttributeError as exc:
                raise ValueError(f"Unknown attribute '{attr}' in placeholder '{{{full_path}}}'") from exc

        # Convert the final value to string
        return str(current_obj)

    # Perform substitution
    try:
        receipt = placeholder_pattern.sub(replace_placeholder, receipt_format)
    except ValueError as exc:
        # Propagate errors related to invalid placeholders or protected access
        raise

    return receipt


# ----------------------------------------------------------------------
# Example data (would normally be loaded elsewhere)
# ----------------------------------------------------------------------
def _populate_example_data():
    cust = Customer(id="c001", name="Alice Smith", email="alice@example.com", _ssn="123-45-6789")
    ord_ = Order(id="o1001", customer_id=cust.id, total=149.99, items=["Widget A", "Gadget B"])
    CUSTOMERS_DB[cust.id] = cust
    ORDERS_DB[ord_.id] = ord_

# Populate example data for demonstration purposes
_populate_example_data()

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = (
#         "Invoice #{invoice_id}\n"
#         "Customer: {customer.name} ({customer.email})\n"
#         "Total: ${order.total}\n"
#     )
#     print(compose_invoice_template("o1001", template.format(invoice_id="001")))