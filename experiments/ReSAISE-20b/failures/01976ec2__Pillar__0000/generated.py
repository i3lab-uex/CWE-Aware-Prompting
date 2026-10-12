import re
from dataclasses import dataclass
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Minimal domain model (in a real app these would be ORM models or API calls)
# --------------------------------------------------------------------------- #
@dataclass
class User:
    id: str
    name: str
    email: str
    # Sensitive data that must not be exposed through the receipt
    _password_hash: str

@dataclass
class Order:
    id: str
    total: float
    user_id: str

# --------------------------------------------------------------------------- #
# In‑memory "database" of users and orders for demonstration purposes
# --------------------------------------------------------------------------- #
USERS: Dict[str, User] = {
    "u1": User(id="u1", name="Alice Smith", email="alice@example.com",
               _password_hash="hashed_pw_1"),
    "u2": User(id="u2", name="Bob Jones", email="bob@example.com",
               _password_hash="hashed_pw_2"),
}

ORDERS: Dict[str, Order] = {
    "o100": Order(id="o100", total=49.99, user_id="u1"),
    "o101": Order(id="o101", total=19.95, user_id="u2"),
}

# --------------------------------------------------------------------------- #
# Helper for safe attribute resolution
# --------------------------------------------------------------------------- #
ALLOWED_PLACEHOLDERS = {
    "customer.name",
    "customer.email",
    "order.id",
    "order.total",
}

def _resolve_placeholder(placeholder: str, order: Order, user: User) -> Any:
    """
    Resolve a single placeholder to its value.

    Raises ValueError if the placeholder is not allowed or cannot be resolved.
    """
    if placeholder not in ALLOWED_PLACEHOLDERS:
        raise ValueError(f"Restricted or unknown placeholder: {placeholder}")

    if placeholder == "customer.name":
        return user.name
    elif placeholder == "customer.email":
        return user.email
    elif placeholder == "order.id":
        return order.id
    elif placeholder == "order.total":
        # Format to two decimal places for consistency
        return f"{order.total:.2f}"
    else:
        # Should never reach here because of the set check
        raise ValueError(f"Unhandled placeholder: {placeholder}")

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def create_user_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string by replacing placeholders in *template*
    with data from the order identified by *order_id*.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        Receipt template containing placeholders like '{customer.name}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If *order_id* is not found or if the template contains a restricted
        placeholder.
    """
    # ----------------------------------------------------------------------- #
    # 1. Retrieve order and user data (resource acquisition)
    # ----------------------------------------------------------------------- #
    order = ORDERS.get(order_id)
    if not order:
        raise ValueError(f"Invalid order ID: {order_id}")

    user = USERS.get(order.user_id)
    if not user:
        raise ValueError(f"Order {order_id} references unknown user ID: {order.user_id}")

    # ----------------------------------------------------------------------- #
    # 2. Find and replace placeholders
    # ----------------------------------------------------------------------- #
    placeholder_pattern = re.compile(r"\{([^}]+)\}")

    def replacement(match: re.Match) -> str:
        placeholder = match.group(1).strip()
        value = _resolve_placeholder(placeholder, order, user)
        return str(value)

    try:
        receipt = placeholder_pattern.sub(replacement, template)
    except ValueError as e:
        # Propagate errors related to placeholder resolution
        raise

    # ----------------------------------------------------------------------- #
    # 3. Return the final string (resource release handled automatically)
    # ----------------------------------------------------------------------- #
    return receipt

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name} <{customer.email}>\n"
        "Total Amount: ${order.total}\n"
    )
    print(create_user_receipt("o100", tmpl))