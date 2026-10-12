import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Mocked domain objects (in a real system these would come from the DB)
# ----------------------------------------------------------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str
    address: str = field(default="")  # sensitive, not allowed in templates


@dataclass
class Order:
    id: str
    total: float
    customer: Customer


# In-memory registries for demo purposes
CUSTOMERS: Dict[str, Customer] = {}
ORDERS: Dict[str, Order] = {}


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
ALLOWED_TOKENS = {
    "customer.name",
    "customer.email",
    "order.id",
    "order.total",
}

# Regex to find placeholders like {customer.name}
PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_.]+)\}")


def _extract_tokens(template: str):
    """Return a set of unique placeholder tokens found in the template."""
    return set(PLACEHOLDER_RE.findall(template))


def _build_context(order: Order):
    """Return a dict that can be used with str.format_map."""
    return {"customer": order.customer, "order": order}


class _SafeFormatter:
    """Custom formatter that validates placeholder names against a whitelist."""

    def __init__(self, allowed_tokens):
        self.allowed = set(allowed_tokens)

    def format(self, template: str, context: dict) -> str:
        tokens = _extract_tokens(template)
        for token in tokens:
            if token not in self.allowed:
                raise ValueError(f"Unauthorized placeholder requested: '{token}'")
        # Use a simple approach: replace tokens manually to avoid exposing
        # attributes beyond the whitelist.
        def repl(match):
            token = match.group(1)
            obj_name, attr_name = token.split(".", 1)
            obj = context[obj_name]
            try:
                return str(getattr(obj, attr_name))
            except AttributeError as exc:
                raise ValueError(f"Invalid attribute in placeholder: '{token}'") from exc

        return PLACEHOLDER_RE.sub(repl, template)


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_receipt_for_transaction(transaction_id: str, template_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the provided template.

    Parameters
    ----------
    transaction_id : str
        The unique identifier of the order.
    template_format : str
        A string containing placeholders such as '{customer.name}'.

    Returns
    -------
    str
        The formatted receipt string with placeholders replaced.

    Raises
    ------
    ValueError
        If the transaction ID does not exist, or if the template contains a
        placeholder that requests restricted data.
    """
    # 1. Retrieve order; raise if not found
    order = ORDERS.get(transaction_id)
    if order is None:
        raise ValueError(f"Order with ID '{transaction_id}' not found")

    # 2. Validate placeholders against whitelist
    formatter = _SafeFormatter(ALLOWED_TOKENS)
    context = _build_context(order)

    # 3. Format the template
    return formatter.format(template_format, context)


# ----------------------------------------------------------------------
# Example usage (for demonstration only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Setup demo data
    cust = Customer(id="c001", name="Alice Smith", email="alice@example.com")
    order = Order(id="o123", total=199.99, customer=cust)
    CUSTOMERS[cust.id] = cust
    ORDERS[order.id] = order

    # Valid template
    tmpl = (
        "Receipt for Order #{order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total Amount: ${order.total}"
    )
    print(create_receipt_for_transaction("o123", tmpl))

    # Invalid template (restricted field)
    bad_tmpl = "Address: {customer.address}"
    try:
        print(create_receipt_for_transaction("o123", bad_tmpl))
    except ValueError as e:
        print(f"Error: {e}")