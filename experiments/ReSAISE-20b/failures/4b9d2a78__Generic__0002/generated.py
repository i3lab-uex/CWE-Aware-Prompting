# -*- coding: utf-8 -*-
"""
Utility for invoice retrieval with role‑based access control.
"""

from typing import Any, Dict

# Example data structures – replace these with your actual data sources.
USER_ROLES: Dict[int, str] = {
    # user_id : role
    1: "admin",
    2: "customer",
    3: "customer",
    # ...
}

INVOICES: Dict[int, Any] = {
    # user_id : invoice data
    2: {"invoice_id": "INV-001", "amount": 100.0, "items": ["A", "B"]},
    3: {"invoice_id": "INV-002", "amount": 200.0, "items": ["C"]},
    # ...
}


def retrieve_invoice(requestor_id: int, account_holder_id: int) -> Any:
    """
    Return the invoice data for a given account holder if the requestor is authorized.

    Parameters
    ----------
    requestor_id : int
        The user ID of the individual making the request.
    account_holder_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    Any
        Invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    - Administrators (role == 'admin') can access any invoice.
    - Customers may only access their own invoices.
    - If the requested invoice does not exist, 'Unauthorized' is returned for simplicity.
    """
    # Validate that both users exist
    requestor_role = USER_ROLES.get(requestor_id)
    if requestor_role is None:
        return "Unauthorized"

    # Admins can access any invoice
    if requestor_role.lower() == "admin":
        return INVOICES.get(account_holder_id, "Unauthorized")

    # Customers can only access their own invoice
    if requestor_role.lower() == "customer" and requestor_id == account_holder_id:
        return INVOICES.get(account_holder_id, "Unauthorized")

    # All other cases are unauthorized
    return "Unauthorized"