# -*- coding: utf-8 -*-

"""
Invoice retrieval module.

The `retrieve_invoice` function checks whether the requesting user is authorized
to download an invoice.  A user can retrieve their own invoice or, if they
have the role of `admin`, any user's invoice.  Unauthorized attempts return
the string 'Unauthorized'.
"""

from typing import Any, Dict

# Example data structures.  In a real application these would be loaded from
# a database or external service.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... additional users
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 120.50, "currency": "USD"},
    3: {"invoice_id": "INV-002", "amount": 89.99,  "currency": "USD"},
    # ... additional invoices
}


def retrieve_invoice(requestor_id: int, account_holder_id: int) -> Any:
    """
    Retrieve an invoice for a user if the requestor is authorized.

    Parameters
    ----------
    requestor_id : int
        The user ID of the individual making the request.
    account_holder_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    Any
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user can access their own invoice.
    - Users with the role 'admin' can access any user's invoice.
    - If either user ID is unknown, the function treats it as unauthorized.
    """
    # Verify that both users exist in the system
    if requestor_id not in USER_ROLES or account_holder_id not in INVOICES:
        return "Unauthorized"

    # Authorization check
    if requestor_id != account_holder_id and USER_ROLES.get(requestor_id) != "admin":
        return "Unauthorized"

    # Fetch the invoice data
    invoice = INVOICES.get(account_holder_id)
    if not invoice:
        return "Unauthorized"

    return invoice