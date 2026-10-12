import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Mocked domain classes (in a real project these would come from the
# application layer)
# ------------------------------------------------------------------
@dataclass
class User:
    id: str
    name: str
    email: str
    # Sensitive attributes that must never be exposed in a receipt
    _ssn: str = field(repr=False, default="")

@dataclass
class Order:
    id: str
    total: float
    currency: str
    customer: User

# ------------------------------------------------------------------
# In‑memory “database” for demo purposes
# ------------------------------------------------------------------
_USERS: Dict[str, User] = {
    "u1": User(id="u1", name="Alice Smith", email="alice@example.com", _ssn="123-45-6789"),
    "u2": User(id="u2", name="Bob Jones", email="bob@example.com"),
}

_ORDERS: Dict[str, Order] = {
    "o100": Order(id="o100", total=149.99, currency="USD", customer=_USERS["u1"]),
    "o101": Order(id="o101", total=79.50, currency="EUR", customer=_USERS["u2"]),
}

# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------
_RESTRICTED_ATTRS = {"_ssn", "password", "credit_card_number"}

def _safe_getattr(obj, attr):
    """
    Retrieve an attribute from *obj* while ensuring that
    restricted attributes cannot be accessed.
    """
    if attr in _RESTRICTED_ATTRS:
        raise ValueError(f"Access to restricted attribute '{attr}' is forbidden.")
    try:
        return getattr(obj, attr)
    except AttributeError as exc:
        raise ValueError(f"Attribute '{attr}' not found on {obj.__class__.__name__}.") from exc

def _build_context(order: Order):
    """
    Build a nested dictionary that mimics the placeholder structure
    (e.g. customer.name, order.total).
    """
    context = {
        "customer": {k: _safe_getattr(order.customer, k) for k in vars(order.customer)},
        "order": {k: _safe_getattr(order, k) for k in vars(order)},
    }
    return context

def _replace_placeholders(template: str, context: Dict):
    """
    Replace placeholders of the form {entity.attribute} in *template*
    with values from *context*. Raises ValueError if a placeholder
    refers to a non‑existent attribute or an attempt is made to
    access restricted data.
    """
    pattern = re.compile(r"{(?P<entity>\w+)\.(?P<attr>[\w_]+)}")

    def repl(match):
        entity = match.group("entity")
        attr   = match.group("attr")
        if entity not in context:
            raise ValueError(f"Unknown placeholder entity '{entity}'.")
        try:
            return str(context[entity][attr])
        except KeyError as exc:
            raise ValueError(f"Attribute '{attr}' not found for entity '{entity}'.") from exc

    return pattern.sub(repl, template)

# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------
def create_user_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt for the given *order_id* by filling in
    placeholders within *template*.

    Parameters:
        order_id (str): The unique identifier of the order.
        template (str): A string containing placeholders such as
                        '{customer.name}' or '{order.total}'.

    Returns:
        str: The formatted receipt string.

    Raises:
        ValueError: If *order_id* is invalid, if a placeholder
                    references non‑existent data, or if there is an
                    attempt to access restricted customer information.
    """
    # Retrieve the order – raise if not found
    try:
        order = _ORDERS[order_id]
    except KeyError as exc:
        raise ValueError(f"Order ID '{order_id}' is invalid.") from exc

    # Build context for safe substitution
    context = _build_context(order)

    # Perform placeholder replacement
    return _replace_placeholders(template, context)