# -*- coding: utf-8 -*-
"""
Utility to fetch invoices with role‑based access control.
"""

from typing import Any, Dict

# Example data – replace these with real storage or database look‑ups.
USER_ROLES: Dict[int, list[str]] = {
    1: ["ADMIN"],
    2: ["CUSTOMER"],
    3: ["CUSTOMER"],
}

INVOICES: Dict[int, dict[str, Any]] = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 175.50, "status": "unpaid"},
}


def _has_role(user_id: int, role: str) -> bool:
    """
    Check whether a user has a specific role.
    """
    return role in USER_ROLES.get(user_id, [])


def fetch_invoice(req_user_id: int, target_cust_id: int) -> Any:
    """
    Retrieve the invoice for `target_cust_id` if the requesting user
    (`req_user_id`) is authorized.

    Parameters
    ----------
    req_user_id : int
        ID of the user making the request.
    target_cust_id : int
        ID of the customer whose invoice is requested.

    Returns
    -------
    dict or str
        The invoice data if authorized; otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID does not exist in the role mapping.
    """
    # Validate existence of both users
    if req_user_id not in USER_ROLES:
        raise KeyError(f"Requesting user ID {req_user_id} not found.")
    if target_cust_id not in USER_ROLES:
        raise KeyError(f"Target customer ID {target_cust_id} not found.")

    # Authorization logic
    if _has_role(req_user_id, "ADMIN") or req_user_id == target_cust_id:
        # Fetch the invoice if it exists
        return INVOICES.get(target_cust_id, "Invoice not found.")
    else:
        return "Unauthorized"