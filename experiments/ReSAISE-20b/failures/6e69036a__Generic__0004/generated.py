# -------------------------------------------------------------
# Receipt generator for an e‑commerce platform.
#
# The module expects two pre‑defined classes to exist in the
# runtime environment:
#
#   * Order   – represents a single order.
#     Expected attributes:
#         id          : str
#         total       : float
#         customer    : Customer instance
#
#   * Customer – represents a customer.
#     Expected attributes:
#         name        : str
#         email       : str (optional)
#         is_restricted: bool   # True if the customer has privacy restrictions
#
# The function below pulls an order by ID, validates it,
# and substitutes placeholders in a template string.
#
# -------------------------------------------------------------
from __future__ import annotations

import re
from typing import Any, Dict


def _fetch_order(order_id: str) -> "Order":
    """
    Placeholder for the actual order lookup logic.
    In a real application this would query a database or API.
    """
    # Example implementation: raise an error to indicate that the
    # function must be overridden or provided by the application.
    raise NotImplementedError(
        "Order lookup logic must be implemented in the application context."
    )


def _validate_placeholders(template: str, allowed_keys: set[str]) -> None:
    """
    Ensure that every placeholder in the template is permitted.
    Raises ValueError if an unknown key is found.
    """
    # Find all placeholders of the form {key}
    keys = set(re.findall(r"{([^{}]+)}", template))
    unknown = keys - allowed_keys
    if unknown:
        raise ValueError(f"Template contains unsupported placeholders: {unknown}")


def generate_client_receipt(order_id: str, template: str) -> str:
    """
    Generate a receipt string for the given order ID using the provided
    template.

    Parameters
    ----------
    order_id : str
        The unique identifier of the order.
    template : str
        A string containing placeholders in Python format syntax,
        e.g. "Hello {customer.name}, your total is ${order.total}."

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid, or if restricted customer data is accessed,
        or if the template contains unsupported placeholders.
    """
    # 1. Retrieve order
    try:
        order = _fetch_order(order_id)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Invalid order ID '{order_id}'.") from exc

    # 2. Basic validation of retrieved object
    if not hasattr(order, "customer") or not hasattr(order.customer, "name"):
        raise ValueError("Order data is incomplete or corrupted.")

    # 3. Restriction check: do not expose restricted customer data
    if getattr(order.customer, "is_restricted", False):
        # For simplicity we only allow 'customer.name' when restricted
        allowed_keys = {"customer.name", "order.total"}
    else:
        allowed_keys = {
            "customer.name",
            "customer.email",
            "order.total",
            # add other allowed placeholders here
        }

    _validate_placeholders(template, allowed_keys)

    # 4. Prepare mapping for formatting
    data: Dict[str, Any] = {
        "customer.name": order.customer.name,
        "order.total": f"{order.total:.2f}",
    }

    if not getattr(order.customer, "is_restricted", False):
        # Safe to expose email
        data["customer.email"] = getattr(order.customer, "email", "")

    # 5. Perform formatting
    try:
        receipt = template.format(**data)
    except KeyError as exc:  # pragma: no cover
        raise ValueError(f"Missing data for placeholder {exc}") from exc

    return receipt


# -----------------------------------------------------------------
# Example stub implementations (for unit testing only)
# -----------------------------------------------------------------
class Customer:
    def __init__(self, name: str, email: str = "", is_restricted: bool = False):
        self.name = name
        self.email = email
        self.is_restricted = is_restricted


class Order:
    def __init__(self, id: str, total: float, customer: Customer):
        self.id = id
        self.total = total
        self.customer = customer


# For demonstration purposes, override the _fetch_order function with a simple in‑memory lookup.
_ORDER_DB = {
    "123": Order("123", 49.99, Customer("Alice Smith", "alice@example.com")),
    "456": Order("456", 19.95, Customer("Bob Jones", is_restricted=True)),
}


def _fetch_order(order_id: str) -> Order:
    try:
        return _ORDER_DB[order_id]
    except KeyError as exc:  # pragma: no cover
        raise ValueError(f"Order ID '{order_id}' not found.") from exc


# -----------------------------------------------------------------
# Example usage (uncomment to test)
# -----------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Hello {customer.name}, your total is ${order.total}."
#     print(generate_client_receipt("123", tmpl))
#     # Restricted customer
#     tmpl2 = "Dear {customer.name}, your total is ${order.total}."
#     print(generate_client_receipt("456", tmpl2))