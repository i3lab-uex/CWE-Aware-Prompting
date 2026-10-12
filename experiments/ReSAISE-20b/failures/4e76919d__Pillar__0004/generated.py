# -*- coding: utf-8 -*-
"""
Secure invoice retrieval module.

Author: ChatGPT
"""

from typing import Any, Dict

# Example data structures (replace with real data in production)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... other users
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.0, "status": "paid"},
    3: {"invoice_id": 102, "amount": 125.5, "status": "unpaid"},
    # ... other invoices
}


def get_invoice(requester_id: int, client_id: int) -> Any:
    """
    Retrieve an invoice for a given client if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the individual making the request.
    client_id : int
        The user ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    * An administrator (role == "admin") can access any invoice.
    * A customer can only access their own invoice.
    * The function does **not** raise exceptions for missing users or invoices;
      it simply returns 'Unauthorized' to avoid leaking information.
    """
    # Fetch roles safely; default to an empty string if user not found
    requester_role = USER_ROLES.get(requester_id, "")

    # Authorization check
    if requester_role != "admin" and requester_id != client_id:
        return "Unauthorized"

    # Retrieve invoice data safely; if not found, also treat as unauthorized
    invoice = INVOICES.get(client_id)
    if invoice is None:
        return "Unauthorized"

    return invoice