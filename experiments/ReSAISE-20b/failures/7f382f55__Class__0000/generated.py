import re
from typing import Any

# ----------------------------------------------------------------------
# Minimal stubs for Order and Customer classes.
# In a real system these would be imported from the e‑commerce domain layer.
# ----------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str, phone: str, ssn: str):
        self.name = name
        self.email = email          # public
        self.phone = phone          # public
        self._ssn = ssn             # protected (sensitive)

    @property
    def ssn(self):
        raise AttributeError("Access to SSN is not permitted")

class Order:
    def __init__(self, order_id: str, customer: Customer, total: float,
                 items: list[str], status: str):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items
        self.status = status

# ----------------------------------------------------------------------
# A tiny in‑memory repository to look up orders by ID.
# In production this would query a database or service.
# ----------------------------------------------------------------------
ORDER_REPOSITORY = {}

def register_order(order: Order):
    ORDER_REPOSITORY[order.order_id] = order

# ----------------------------------------------------------------------
# Helper to safely retrieve attributes from objects.
# Raises ValueError if the attribute is protected or does not exist.
# ----------------------------------------------------------------------
def _safe_getattr(obj: Any, attr: str) -> Any:
    if attr.startswith('_'):
        raise ValueError(f"Attempt to access protected attribute '{attr}'")
    if not hasattr(obj, attr):
        raise ValueError(f"Attribute '{attr}' does not exist on {type(obj).__name__}")
    return getattr(obj, attr)

# ----------------------------------------------------------------------
# Main function: compose_invoice_template
# ----------------------------------------------------------------------
def compose_invoice_template(invoice_id: str, receipt_format: str) -> str:
    """
    Generate a receipt string for the given order ID using the supplied
    template. The template may contain placeholders in the form
    `{object.attribute}` where `object` is either `customer` or `order`.

    Parameters
    ----------
    invoice_id : str
        The unique identifier of the order.
    receipt_format : str
        Template string containing placeholders.

    Returns
    -------
    str
        The formatted receipt string with all placeholders replaced by the
        corresponding values.

    Raises
    ------
    ValueError
        If the order ID is invalid or if the template tries to access a
        protected attribute.
    """
    # Validate order ID and fetch order
    if invoice_id not in ORDER_REPOSITORY:
        raise ValueError(f"Invalid order ID: {invoice_id}")
    order = ORDER_REPOSITORY[invoice_id]
    customer = order.customer

    # Regular expression to find placeholders like {customer.name}
    placeholder_pattern = re.compile(r'\{(\w+)\.(\w+)\}')

    def replace_placeholder(match: re.Match) -> str:
        obj_name, attr = match.group(1), match.group(2)
        # Determine which object the placeholder refers to
        if obj_name == 'customer':
            value = _safe_getattr(customer, attr)
        elif obj_name == 'order':
            value = _safe_getattr(order, attr)
        else:
            raise ValueError(f"Unknown placeholder object '{obj_name}'")
        # Convert value to string for insertion
        return str(value)

    try:
        receipt = placeholder_pattern.sub(replace_placeholder, receipt_format)
    except ValueError as exc:
        # Re‑raise to match the function contract
        raise

    return receipt

# ----------------------------------------------------------------------
# Example usage (for demonstration only – remove or guard in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Create a customer and order
    cust = Customer(name="Jane Doe", email="jane@example.com",
                    phone="555-1234", ssn="123-45-6789")
    ord1 = Order(order_id="INV001", customer=cust,
                 total=199.99, items=["Widget A", "Widget B"], status="Shipped")
    register_order(ord1)

    template = (
        "Invoice #{invoice_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Phone: {customer.phone}\n"
        "Total: ${order.total}\n"
        "Status: {order.status}"
    )

    # Replace placeholder for invoice_id manually since it's not part of the
    # object mapping (could also be added to the pattern if desired)
    formatted_template = template.format(invoice_id=ord1.order_id)

    try:
        receipt_text = compose_invoice_template("INV001", formatted_template)
        print(receipt_text)
    except ValueError as e:
        print(f"Error generating receipt: {e}")