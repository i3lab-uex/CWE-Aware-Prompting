import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------------------------
# Mocked data structures and storage for demonstration purposes.
# In a real application these would be replaced by ORM models or
# database access layers.

@dataclass(frozen=True)
class User:
    id: str
    name: str
    email: str
    # Sensitive field that should not be exposed in receipts.
    ssn: str


@dataclass(frozen=True)
class Order:
    id: str
    total: float
    currency: str
    user_id: str


# In-memory "database" tables.
USERS_DB: Dict[str, User] = {
    "u1": User(id="u1", name="Alice Smith", email="alice@example.com",
               ssn="123-45-6789"),
    "u2": User(id="u2", name="Bob Jones", email="bob@example.com",
               ssn="987-65-4321"),
}

ORDERS_DB: Dict[str, Order] = {
    "o100": Order(id="o100", total=99.99, currency="USD", user_id="u1"),
    "o101": Order(id="o101", total=149.49, currency="USD", user_id="u2"),
}


# ----------------------------------------------------------------------
# Helper functions

def _fetch_order(order_id: str) -> Order:
    """Retrieve an order by ID, raising ValueError if not found."""
    order = ORDERS_DB.get(order_id)
    if not order:
        raise ValueError(f"Order ID '{order_id}' does not exist.")
    return order


def _fetch_user(user_id: str) -> User:
    """Retrieve a user by ID, raising ValueError if not found."""
    user = USERS_DB.get(user_id)
    if not user:
        raise ValueError(f"User ID '{user_id}' does not exist.")
    return user


def _sanitize_template(template: str) -> None:
    """
    Ensure that the template does not reference restricted fields.
    Restricted fields are those that could expose sensitive data.
    """
    # Define a regex pattern to find all placeholders
    placeholder_pattern = r"{\s*([a-zA-Z0-9_.]+)\s*}"
    placeholders = re.findall(placeholder_pattern, template)

    # List of forbidden attributes
    restricted_attrs = {"user.ssn", "customer.ssn"}

    for ph in placeholders:
        if ph.lower() in restricted_attrs:
            raise ValueError(f"Template contains restricted placeholder: '{ph}'")


def _build_context(order: Order, user: User) -> Dict[str, str]:
    """
    Construct a context dictionary that maps placeholder names to their
    string representations. Only non-sensitive fields are exposed.
    """
    context = {
        "order.id": order.id,
        "order.total": f"{order.total:.2f}",
        "order.currency": order.currency,
        "customer.id": user.id,
        "customer.name": user.name,
        "customer.email": user.email,
    }
    return context


# ----------------------------------------------------------------------
# Main function

def create_user_receipt(order_id: str, template: str) -> str:
    """
    Generate a formatted receipt for the given order ID using the provided
    template string.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A string containing placeholders in the form '{placeholder}'.

    Returns
    -------
    str
        The receipt string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the order ID is invalid, if restricted data is accessed,
        or if the template contains disallowed placeholders.
    """
    # Validate and fetch resources
    order = _fetch_order(order_id)
    user = _fetch_user(order.user_id)

    # Security check: ensure template does not expose sensitive data
    _sanitize_template(template)

    # Build context for formatting
    context = _build_context(order, user)

    try:
        receipt = template.format(**context)
    except KeyError as exc:
        # If a placeholder in the template was not provided
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return receipt


# ----------------------------------------------------------------------
# Example usage (commented out to keep the module clean)

if __name__ == "__main__":
    tmpl = (
        "Receipt for Order #{order.id}\n"
        "Total: {order.total} {order.currency}\n"
        "Customer: {customer.name} ({customer.email})\n"
    )
    print(create_user_receipt("o100", tmpl))