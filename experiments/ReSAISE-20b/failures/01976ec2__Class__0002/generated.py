import re
from dataclasses import dataclass
from typing import Dict, Any

# --------------------------------------------------------------------
# Mocked domain classes (would normally come from the application)
# --------------------------------------------------------------------

@dataclass
class User:
    id: str
    name: str
    email: str          # Sensitive
    phone: str          # Sensitive

@dataclass
class Order:
    id: str
    total: float
    customer: User

# --------------------------------------------------------------------
# In‑memory “repository” – in a real app this would query a DB
# --------------------------------------------------------------------
_ORDER_DB: Dict[str, Order] = {}

def get_order(order_id: str) -> Order | None:
    """Retrieve an order by its ID, or return None if not found."""
    return _ORDER_DB.get(order_id)

# --------------------------------------------------------------------
# Core function
# --------------------------------------------------------------------

_PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

def create_user_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt by filling in placeholders from the given template.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        String containing placeholders like `{customer.name}` or `{order.total}`.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if a restricted field is requested.
    """
    # 1. Validate the order ID
    order = get_order(order_id)
    if order is None:
        raise ValueError(f"Order ID '{order_id}' does not exist.")

    # 2. Build a safe mapping of allowed values
    #    Only expose non‑sensitive fields.
    allowed_map: Dict[str, Any] = {
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "customer.name": order.customer.name,
    }

    # 3. Replace placeholders safely
    def _replace(match: re.Match) -> str:
        key = match.group(1)
        if key not in allowed_map:
            # If the placeholder refers to a restricted field, refuse
            raise ValueError(f"Access to '{key}' is not permitted.")
        return str(allowed_map[key])

    try:
        receipt = _PLACEHOLDER_RE.sub(_replace, template)
    except re.error as exc:
        # Should not happen; defensive
        raise ValueError(f"Invalid template syntax: {exc}") from exc

    return receipt


# --------------------------------------------------------------------
# Example usage (for demonstration only – remove in production)
# --------------------------------------------------------------------

if __name__ == "__main__":
    # Populate the mock DB
    user = User(id="u123", name="Alice Smith", email="alice@example.com", phone="+1234567890")
    order = Order(id="o456", total=149.99, customer=user)
    _ORDER_DB[order.id] = order

    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name}\n"
        "Total Amount: ${order.total}"
    )

    print(create_user_receipt("o456", tmpl))