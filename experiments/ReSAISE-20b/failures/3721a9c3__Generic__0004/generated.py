# -*- coding: utf-8 -*-
"""
Utility to generate buyer receipts from a template.

The function expects the following pre‑defined classes to be available in
the runtime environment:

- `Order` – represents an e‑commerce order.  It must expose at least the
  following attributes/methods:
    * `order.id` – unique identifier (string)
    * `order.total` – total amount for the order
    * `order.customer` – a :class:`Customer` instance associated with the
      order
    * `Order.get_by_id(order_id: str) -> Order` – class method that retrieves
      an order or raises ``KeyError`` if the id is unknown.

- `Customer` – represents a customer.  It must expose at least:
    * `customer.name`
    * `customer.email`

Only these fields are considered safe for interpolation.  Any attempt to
access other customer attributes (e.g., ``ssn``) will raise a :class:`ValueError`.

The template string may contain placeholders such as ``{customer.name}``
or ``{order.total}``.  The function replaces them with the corresponding
values and returns the fully formatted receipt string.

"""

from __future__ import annotations

import re
from typing import Any, Dict


# --------------------------------------------------------------------------- #
# Helper: safe placeholder extraction
# --------------------------------------------------------------------------- #

PLACEHOLDER_RE = re.compile(r"{(?P<field>[^}]+)}")


def _extract_placeholders(template: str) -> set[str]:
    """
    Return a set of unique placeholder names found in *template*.
    """
    return {m.group("field") for m in PLACEHOLDER_RE.finditer(template)}


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def generate_buyer_receipt(order_id: str, template: str) -> str:
    """
    Generate a buyer receipt by filling *template* with data from the
    order identified by *order_id*.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        Receipt template containing placeholders in the form
        ``{customer.name}``, ``{order.total}``, etc.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If *order_id* is invalid or if the template tries to access a
        restricted customer attribute.
    KeyError
        If the template contains placeholders that cannot be resolved.
    """
    # --------------------------------------------------- #
    # 1. Retrieve the order
    # --------------------------------------------------- #
    try:
        order = Order.get_by_id(order_id)  # type: ignore[attr-defined]
    except KeyError as exc:
        raise ValueError(f"Invalid order ID: {order_id}") from exc

    # --------------------------------------------------- #
    # 2. Prepare the context dictionary
    # --------------------------------------------------- #
    customer = order.customer  # type: ignore[attr-defined]

    context: Dict[str, Any] = {
        "order.id": order.id,
        "order.total": getattr(order, "total", None),
        # Basic customer fields – adjust as necessary
        "customer.name": getattr(customer, "name", None),
        "customer.email": getattr(customer, "email", None),
    }

    # --------------------------------------------------- #
    # 3. Detect disallowed placeholders
    # --------------------------------------------------- #
    placeholders = _extract_placeholders(template)
    for ph in placeholders:
        if not any(ph == key or ph.startswith(key + ".") for key in context):
            # If the placeholder is a customer attribute that is not allowed
            if ph.startswith("customer.") and not any(
                ph == key or ph.startswith(key + ".") for key in context
            ):
                raise ValueError(
                    f"Attempt to access restricted customer data: '{ph}'"
                )
            # Unknown placeholder – will be caught later
            continue

    # --------------------------------------------------- #
    # 4. Perform formatting
    # --------------------------------------------------- #
    try:
        receipt = template.format(**context)
    except KeyError as exc:
        missing = exc.args[0]
        raise ValueError(f"Missing data for placeholder: '{missing}'") from exc

    return receipt