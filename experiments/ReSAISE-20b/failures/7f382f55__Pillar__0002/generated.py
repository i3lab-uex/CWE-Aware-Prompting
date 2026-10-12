import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Mock data models (in a real system these would come from your ORM)
# ----------------------------------------------------------------------


@dataclass
class Customer:
    id: str
    name: str
    email: str
    _ssn: str = field(repr=False)  # protected attribute


@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: Dict[str, int]  # item name -> quantity


# ----------------------------------------------------------------------
# In‑memory "database" of customers and orders
# ----------------------------------------------------------------------


CUSTOMERS: Dict[str, Customer] = {
    "cust-001": Customer(id="cust-001", name="Alice Smith",
                         email="alice@example.com", _ssn="123-45-6789"),
    "cust-002": Customer(id="cust-002", name="Bob Jones",
                         email="bob@example.com", _ssn="987-65-4321"),
}

ORDERS: Dict[str, Order] = {
    "order-100": Order(id="order-100", customer_id="cust-001",
                       total=99.95, items={"Widget": 2, "Gadget": 1}),
    "order-101": Order(id="order-101", customer_id="cust-002",
                       total=149.50, items={"Thingamajig": 3}),
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------


def _get_order(order_id: str) -> Order:
    """Retrieve an order or raise ValueError if not found."""
    try:
        return ORDERS[order_id]
    except KeyError as exc:
        raise ValueError(f"Invalid order ID: {order_id}") from exc


def _get_customer(customer_id: str) -> Customer:
    """Retrieve a customer or raise ValueError if not found."""
    try:
        return CUSTOMERS[customer_id]
    except KeyError as exc:
        raise ValueError(f"Invalid customer ID: {customer_id}") from exc


# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------


def compose_invoice_template(invoice_id: str, receipt_format: str) -> str:
    """
    Generate a formatted invoice string for the given order ID.

    Parameters
    ----------
    invoice_id : str
        Identifier of the order to be invoiced.
    receipt_format : str
        Template string containing placeholders such as `{customer.name}` or
        `{order.total}`.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if a protected attribute (starting with
        an underscore) is requested in the template.
    """
    # ------------------------------------------------------------------
    # 1. Load order and customer
    # ------------------------------------------------------------------
    order = _get_order(invoice_id)
    customer = _get_customer(order.customer_id)

    # ------------------------------------------------------------------
    # 2. Prepare mapping for placeholders
    # ------------------------------------------------------------------
    # Map of object names to actual objects (order, customer)
    context = {
        "order": order,
        "customer": customer
    }

    # ------------------------------------------------------------------
    # 3. Find all placeholders in the template
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{([a-zA-Z_][\w\.]*)\}")
    placeholders = placeholder_pattern.findall(receipt_format)

    # ------------------------------------------------------------------
    # 4. Resolve each placeholder
    # ------------------------------------------------------------------
    resolved = {}
    for token in placeholders:
        # Guard against protected attributes (starting with '_')
        if any(part.startswith("_") for part in token.split(".")):
            raise ValueError(f"Attempt to access protected attribute: {token}")

        # Resolve token like 'customer.name' or 'order.total'
        parts = token.split(".")
        obj_name, attr_chain = parts[0], parts[1:]

        try:
            value = context[obj_name]
        except KeyError as exc:
            raise ValueError(f"Unknown placeholder object: {obj_name}") from exc

        for attr in attr_chain:
            try:
                value = getattr(value, attr)
            except AttributeError as exc:
                raise ValueError(f"Invalid attribute '{attr}' in placeholder "
                                 f"'{token}'") from exc

        resolved[token] = value

    # ------------------------------------------------------------------
    # 5. Perform safe substitution
    # ------------------------------------------------------------------
    def _replacement(match: re.Match) -> str:
        key = match.group(1)
        return str(resolved[key])

    final_receipt = placeholder_pattern.sub(_replacement, receipt_format)
    return final_receipt


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------


if __name__ == "__main__":
    template = (
        "Invoice #{invoice_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total}\n"
        "Items:\n"
        "{items}"
    )

    # Simple items formatting
    def format_items(order: Order) -> str:
        return "\n".join(f"  - {name} x{qty}" for name, qty in order.items.items())

    # Build a full template by inserting items manually
    invoice_id = "order-100"
    order_obj = _get_order(invoice_id)
    items_str = format_items(order_obj)

    full_template = template.format(
        invoice_id=invoice_id,
        items=items_str
    )

    print(compose_invoice_template(invoice_id, full_template))