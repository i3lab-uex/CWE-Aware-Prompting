# -*- coding: utf-8 -*-
"""
Invoice retrieval module.

Provides the `retrieve_invoice` function which enforces access control
based on user roles.  The implementation follows the principle of
least privilege to mitigate CWE-284 (Improper Access Control).

Author: ChatGPT
"""

from typing import Any, Dict

# ----------------------------------------------------------------------
# Sample data structures (replace with real database look‑ups in production)
# ----------------------------------------------------------------------
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... other users
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "items": ["Widget A", "Widget B"]},
    3: {"invoice_id": 102, "amount": 175.50, "items": ["Widget C"]},
    # ... other invoices
}

# ----------------------------------------------------------------------
# Exceptions
# ----------------------------------------------------------------------
class UnauthorizedError(Exception):
    """Raised when a user is not authorized to access the requested resource."""
    pass

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def retrieve_invoice(requestor_id: int, account_holder_id: int) -> Any:
    """
    Return the invoice data for a given account holder if the requestor
    is authorized.

    Parameters
    ----------
    requestor_id : int
        The user ID of the individual making the request.
    account_holder_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    Any
        The invoice data associated with `account_holder_id`.

    Raises
    ------
    UnauthorizedError
        If the requestor does not have permission to view the invoice.
    KeyError
        If either the requestor or account holder does not exist in the system.
    """
    # Verify that both users exist
    if requestor_id not in USER_ROLES:
        raise KeyError(f"Requestor ID {requestor_id} not found.")
    if account_holder_id not in USER_ROLES:
        raise KeyError(f"Account holder ID {account_holder_id} not found.")

    # Check role: admin can access any invoice, otherwise only self
    requestor_role = USER_ROLES[requestor_id]
    if requestor_role != "admin" and requestor_id != account_holder_id:
        raise UnauthorizedError("Unauthorized")

    # Retrieve the invoice; if missing, return None or raise KeyError
    try:
        invoice = INVOICES[account_holder_id]
    except KeyError as exc:
        raise KeyError(f"Invoice for user ID {account_holder_id} not found.") from exc

    return invoice