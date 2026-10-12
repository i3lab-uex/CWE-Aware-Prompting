# -*- coding: utf-8 -*-
"""
Invoice download helper.

This module provides a single function `download_invoice` that enforces
proper access control before returning invoice data. It checks whether the
requesting user is either:
    1) The owner of the invoice, or
    2) An administrator (role 'admin').

If neither condition is met, the function returns the string 'Unauthorized'.

The implementation guards against missing keys and avoids leaking
information about non‑existent invoices.
"""

from typing import Any, Dict

# Example data structures; replace with actual data sources in production.
USER_ROLES: Dict[int, list[str]] = {
    1: ['admin'],
    2: ['customer'],
    3: ['customer'],
    # ...
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00},
    3: {"invoice_id": 102, "amount": 125.50},
    # ...
}


def download_invoice(current_user_id: int, customer_id: int) -> Any:
    """
    Return the invoice data for a given customer if the request is authorized.

    Parameters
    ----------
    current_user_id : int
        The user ID of the actor making the request.
    customer_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    Any
        The invoice data if authorized, otherwise the string 'Unauthorized'.
    """
    # Quick check: if requesting their own invoice
    if current_user_id == customer_id:
        return INVOICES.get(customer_id, "Unauthorized")

    # Check if the current user is an administrator
    roles = USER_ROLES.get(current_user_id, [])
    if "admin" in roles:
        return INVOICES.get(customer_id, "Unauthorized")

    # If neither condition is met, deny access
    return "Unauthorized"