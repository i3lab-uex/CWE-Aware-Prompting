# -*- coding: utf-8 -*-
"""
Utility for secure invoice retrieval.

The module defines a single function `fetch_invoice` that checks the role of
the requesting user and returns the requested invoice if access is permitted.
"""

# Standard library imports
from typing import Any, Dict

# --------------------------------------------------------------------------- #
# Example data – in real usage these would come from a database or other
# persistent storage.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": "INV-001", "amount": 250.0, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 150.0, "status": "unpaid"},
}

# --------------------------------------------------------------------------- #
def fetch_invoice(req_user_id: int, target_cust_id: int) -> Any:
    """
    Retrieve an invoice for a specific customer.

    Parameters
    ----------
    req_user_id : int
        The user ID of the person attempting to access the invoice.
    target_cust_id : int
        The user ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice dictionary if the requester is authorized, otherwise
        the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If the target customer ID does not exist in `INVOICES`.
    """
    # Verify that the target invoice exists
    if target_cust_id not in INVOICES:
        raise KeyError(f"Invoice for customer ID {target_cust_id} not found.")

    # Determine the role of the requesting user
    requester_role = USER_ROLES.get(req_user_id, None)

    # Authorization logic:
    # - Admins can access any invoice.
    # - Regular customers can only access their own invoice.
    if requester_role == "admin" or req_user_id == target_cust_id:
        return INVOICES[target_cust_id]

    # All other cases are unauthorized
    return "Unauthorized"