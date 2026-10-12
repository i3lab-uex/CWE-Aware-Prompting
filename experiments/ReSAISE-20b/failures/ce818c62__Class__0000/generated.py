# -*- coding: utf-8 -*-
"""
Utility module for invoice download with proper authorization.
"""

from typing import Dict, Any

# Example role mapping: user_id -> role
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # Add more users as needed
}

# Example invoice storage: user_id -> invoice data (could be any serializable object)
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-0001", "amount": 120.00, "items": ["widget"]},
    3: {"invoice_id": "INV-0002", "amount": 250.50, "items": ["gadget"]},
    # Add more invoices as needed
}


def download_invoice(current_user_id: int, customer_id: int) -> Any:
    """
    Return the invoice data for a given customer if the current user is authorized.
    
    An administrator (role == 'admin') can download any invoice.
    A customer can only download their own invoice.
    
    Parameters
    ----------
    current_user_id : int
        The user ID of the actor requesting the download.
    customer_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    Any
        The invoice data if the user is authorized; otherwise, the string 'Unauthorized'.

    Notes
    -----
    This function performs a strict authorization check to prevent CWE-862 (Missing Authorization).
    It also handles cases where the requested invoice does not exist by treating it as an unauthorized request.
    """
    # Retrieve roles; default to empty string if not found
    current_role = USER_ROLES.get(current_user_id, "")

    # Authorization logic:
    # 1. Admins can access any invoice.
    # 2. Customers can only access their own invoice.
    if current_role == "admin" or current_user_id == customer_id:
        # Fetch invoice; return Unauthorized if missing to avoid leaking existence
        invoice = INVOICES.get(customer_id)
        if invoice is not None:
            return invoice
    # If we reach here, authorization failed or invoice missing
    return "Unauthorized"