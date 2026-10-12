# -*- coding: utf-8 -*-

from typing import Any, Dict

# Example role mapping and invoice storage
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.0, "status": "paid"},
    3: {"invoice_id": 102, "amount": 175.5, "status": "unpaid"},
}

def access_invoice(user_attempt_id: int, cust_id: int) -> Any:
    """
    Return the invoice data for *cust_id* if *user_attempt_id* is authorized
    to access it. Administrators can retrieve any invoice; customers may only
    retrieve their own.

    Parameters
    ----------
    user_attempt_id : int
        The ID of the user attempting to access the invoice.
    cust_id : int
        The customer whose invoice is being requested.

    Returns
    -------
    Any
        Invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    - Raises no exceptions; missing user or invoice entries are treated as
      unauthorized access.
    """
    # Verify that both users exist in the role mapping
    user_role = USER_ROLES.get(user_attempt_id)
    if user_role is None:
        return "Unauthorized"

    # Allow admin to access any invoice
    if user_role.lower() == "admin":
        return INVOICES.get(cust_id, "Unauthorized")

    # Allow customers to access only their own invoice
    if user_attempt_id == cust_id:
        return INVOICES.get(cust_id, "Unauthorized")

    # Default to unauthorized
    return "Unauthorized"