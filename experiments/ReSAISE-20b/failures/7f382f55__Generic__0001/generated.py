import re
from typing import Any

# ----------------------------------------------------------------------
# Mock data models (in a real system these would be provided elsewhere)
# ----------------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class Order:
    def __init__(self, order_id: str, total: float, customer: Customer):
        self.id = order_id
        self.total = total
        self.customer = customer

# In‑memory "database" of orders for demo purposes
ORDERS_DB = {
    "INV001": Order("INV001", 199.99, Customer("Alice Smith", "alice@example.com")),
    "INV002": Order("INV002", 49.50, Customer("Bob Jones", "bob@example.com")),
}

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def compose_invoice_template(invoice_id: str, receipt_format: str) -> str:
    """
    Generate a formatted invoice string for the given order ID.

    Parameters
    ----------
    invoice_id : str
        Identifier of the order to generate an invoice for.
    receipt_format : str
        Template string containing placeholders like '{customer.name}' or
        '{order.total}'. Placeholders may reference attributes of the Order
        instance or its associated Customer.

    Returns
    -------
    str
        The formatted invoice string with all placeholders replaced by the
        corresponding values.

    Raises
    ------
    ValueError
        If `invoice_id` does not correspond to a known order.
        If a placeholder references a protected attribute (starting with '_')
        or an attribute that does not exist on the target object.
    """
    # 1. Retrieve the order
    order = ORDERS_DB.get(invoice_id)
    if not order:
        raise ValueError(f"Invalid invoice ID: {invoice_id}")

    # 2. Prepare a mapping for safe attribute access
    def _safe_attr(obj: Any, attr_name: str) -> Any:
        if attr_name.startswith("_"):
            raise ValueError(f"Attempt to access protected attribute '{attr_name}'")
        if not hasattr(obj, attr_name):
            raise ValueError(f"Attribute '{attr_name}' not found on {obj.__class__.__name__}")
        return getattr(obj, attr_name)

    # 3. Replace placeholders
    pattern = re.compile(r"\{([^{}]+)\}")

    def _replace(match: re.Match) -> str:
        expr = match.group(1).strip()
        parts = expr.split(".")
        if not parts:
            return match.group(0)

        # Resolve the root object
        if parts[0] == "order":
            obj = order
        elif parts[0] == "customer":
            obj = order.customer
        else:
            raise ValueError(f"Unknown placeholder root '{parts[0]}' in {expr}")

        # Resolve successive attributes
        for attr in parts[1:]:
            obj = _safe_attr(obj, attr)

        # Convert final value to string
        return str(obj)

    result = pattern.sub(_replace, receipt_format)
    return result

# ----------------------------------------------------------------------
# Example usage
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Invoice #{invoice_id}\n"
        "Customer: {customer.name} <{customer.email}>\n"
        "Total Amount: ${order.total}\n"
    )
    print(compose_invoice_template("INV001", template.format(invoice_id="INV001")))