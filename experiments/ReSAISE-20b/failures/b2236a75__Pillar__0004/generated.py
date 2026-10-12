import re
from dataclasses import dataclass, field
from typing import Dict, Any

# --------------------------------------------------------------------------- #
#  Domain models (simplified)                                               #
# --------------------------------------------------------------------------- #

@dataclass
class Customer:
    id: str
    name: str
    email: str
    phone: str
    # Sensitive fields that must never be exposed in a receipt
    _ssn: str = field(repr=False, default="")

@dataclass
class Order:
    id: str
    total: float
    currency: str
    status: str
    # Sensitive fields that must never be exposed in a receipt
    _credit_card_number: str = field(repr=False, default="")

# --------------------------------------------------------------------------- #
#  Mock data store (in a real system this would be database access)         #
# --------------------------------------------------------------------------- #

CUSTOMERS: Dict[str, Customer] = {
    "c001": Customer(id="c001", name="Alice Smith", email="alice@example.com",
                     phone="+1234567890", _ssn="111-22-3333"),
}

ORDERS: Dict[str, Order] = {
    "o100": Order(id="o100", total=49.99, currency="USD", status="completed",
                  _credit_card_number="4111111111111111"),
}

def get_order_by_id(order_id: str) -> Order:
    try:
        return ORDERS[order_id]
    except KeyError as exc:
        raise ValueError(f"Order with id '{order_id}' not found") from exc

def get_customer_by_order(order: Order) -> Customer:
    # In a real system, there would be an order.customer_id field.
    # For this example we simply return a fixed customer for demo purposes.
    try:
        return CUSTOMERS["c001"]
    except KeyError as exc:
        raise ValueError("Associated customer not found") from exc

# --------------------------------------------------------------------------- #
#  Receipt generation                                                       #
# --------------------------------------------------------------------------- #

# Whitelist of attributes that are allowed to appear in the receipt
ALLOWED_ORDER_ATTRS = {"id", "total", "currency", "status"}
ALLOWED_CUSTOMER_ATTRS = {"id", "name", "email", "phone"}

PLACEHOLDER_RE = re.compile(r"\{(?P<obj>\w+)\.(?P<attr>[\w_]+)\}")

def _safe_get_attr(obj: Any, attr: str, allowed_attrs: set) -> Any:
    """
    Retrieve an attribute from `obj` only if it is in the allowed set.
    Raises ValueError for disallowed access.
    """
    if attr not in allowed_attrs:
        raise ValueError(f"Access to disallowed attribute '{attr}'")
    return getattr(obj, attr)

def generate_customer_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order ID using the supplied template.

    The template may contain placeholders in the form `{order.total}` or
    `{customer.name}`. Only a whitelisted set of attributes can be used in the
    template to prevent leaking sensitive data.

    Parameters
    ----------
    order_id : str
        Identifier of the order to generate a receipt for.
    template : str
        Receipt template containing placeholders.

    Returns
    -------
    str
        The rendered receipt string with all placeholders replaced by actual values.

    Raises
    ------
    ValueError
        If the order or customer cannot be found, if a placeholder references an
        attribute that is not allowed, or if any other error occurs during rendering.
    """
    try:
        order = get_order_by_id(order_id)
        customer = get_customer_by_order(order)

        def replace_match(match: re.Match) -> str:
            obj_name = match.group("obj")
            attr_name = match.group("attr")

            if obj_name == "order":
                value = _safe_get_attr(order, attr_name, ALLOWED_ORDER_ATTRS)
            elif obj_name == "customer":
                value = _safe_get_attr(customer, attr_name, ALLOWED_CUSTOMER_ATTRS)
            else:
                raise ValueError(f"Unknown placeholder object '{obj_name}'")

            # Convert non-string values to string (e.g., float formatting)
            if isinstance(value, float):
                # Default two‑decimal precision
                return f"{value:.2f}"
            return str(value)

        receipt = PLACEHOLDER_RE.sub(replace_match, template)
        return receipt

    except Exception as exc:
        # Re‑raise known ValueError, otherwise wrap generic exceptions
        if isinstance(exc, ValueError):
            raise
        raise ValueError(f"Failed to generate receipt: {exc}") from exc

# --------------------------------------------------------------------------- #
#  Example usage (commented out – for illustration only)                    #
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     tmpl = (
#         "Receipt for Order {order.id}\n"
#         "Customer: {customer.name} ({customer.email})\n"
#         "Total: {order.total} {order.currency}\n"
#         "Status: {order.status}"
#     )
#     print(generate_customer_receipt("o100", tmpl))