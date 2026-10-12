import re
from typing import Dict

# --------------------------------------------------------------------
# Dummy in‑memory data stores (replace with real persistence layers)
# --------------------------------------------------------------------

class User:
    def __init__(self, user_id: str, name: str, email: str, is_restricted: bool = False):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.is_restricted = is_restricted

class Order:
    def __init__(self, order_id: str, user: User, total: float, items: list):
        self.order_id = order_id
        self.user = user
        self.total = total
        self.items = items

# Example data (for demonstration purposes only)
_USERS: Dict[str, User] = {
    "u1": User("u1", "Alice Smith", "alice@example.com"),
    "u2": User("u2", "Bob Jones", "bob@example.com", is_restricted=True),
}

_ORDERS: Dict[str, Order] = {
    "o100": Order("o100", _USERS["u1"], 149.99, ["Widget A", "Widget B"]),
    "o200": Order("o200", _USERS["u2"], 79.50, ["Gadget X"]),
}

# --------------------------------------------------------------------
# Helper utilities
# --------------------------------------------------------------------

PLACEHOLDER_PATTERN = re.compile(r"{([a-zA-Z_][\w\.]*)}")

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in PLACEHOLDER_PATTERN.finditer(template)}

def _build_context(order: Order) -> dict:
    """Build a mapping of placeholder names to values for formatting."""
    ctx = {
        "order.id": order.order_id,
        "order.total": f"{order.total:.2f}",
        "order.items": ", ".join(order.items),
    }
    user = order.user
    ctx.update({
        "customer.id": user.user_id,
        "customer.name": user.name,
        "customer.email": user.email,
    })
    return ctx

def _safe_format(template: str, context: dict) -> str:
    """
    Safely replace placeholders in the template with values from the context.
    Raises ValueError if an undefined placeholder is encountered.
    """
    def repl(match):
        key = match.group(1)
        if key not in context:
            raise ValueError(f"Unknown placeholder '{key}' in template.")
        return str(context[key])

    return PLACEHOLDER_PATTERN.sub(repl, template)

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def create_user_receipt(order_id: str, template: str) -> str:
    """
    Generate a formatted receipt for the given order ID using the provided template.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A string containing placeholders such as '{customer.name}' or '{order.total}'.

    Returns
    -------
    str
        The fully formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid, if restricted customer data would be exposed,
        or if the template contains an undefined placeholder.
    """
    # Validate and retrieve order
    order = _ORDERS.get(order_id)
    if not order:
        raise ValueError(f"Order ID '{order_id}' is invalid or does not exist.")

    # Security check: do not expose restricted customer data
    if order.user.is_restricted:
        raise ValueError("Access to restricted customer data is prohibited.")

    # Build context for placeholders
    context = _build_context(order)

    # Validate that all placeholders in the template are known
    missing_placeholders = _extract_placeholders(template) - context.keys()
    if missing_placeholders:
        raise ValueError(f"Template contains unknown placeholders: {missing_placeholders}")

    # Perform safe formatting
    receipt = _safe_format(template, context)
    return receipt

# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = (
        "Receipt for Order #{order.id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Items: {order.items}\n"
        "Total: ${order.total}"
    )
    print(create_user_receipt("o100", tmpl))