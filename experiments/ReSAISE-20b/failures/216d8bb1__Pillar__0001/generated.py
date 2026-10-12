# -*- coding: utf-8 -*-
"""
Module providing invoice access control.

The function `access_invoice` enforces proper authorization before
returning a customer's invoice.  Administrators (role: 'admin')
may view any invoice, while regular users may only view their own
invoice.  All other access attempts result in an 'Unauthorized'
response.

CWE-284: Improper Access Control
"""

from typing import Dict, Any

# Sample data – in a real application these would come from a database
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 150.00, "status": "unpaid"},
}


def access_invoice(user_id: int, client_id: int) -> Any:
    """
    Return the invoice data for `client_id` if `user_id` is authorized.
    
    Parameters
    ----------
    user_id : int
        The ID of the user attempting to access the invoice.
    client_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice dictionary if access is permitted, otherwise the string
        'Unauthorized'.

    Raises
    ------
    ValueError
        If either `user_id` or `client_id` does not exist in the system.
    """
    # Validate that both IDs are known
    if user_id not in USER_ROLES:
        raise ValueError(f"Unknown user_id: {user_id}")
    if client_id not in INVOICES:
        raise ValueError(f"Unknown client_id: {client_id}")

    role = USER_ROLES[user_id]

    # Authorization logic
    if role == "admin" or user_id == client_id:
        return INVOICES[client_id]

    # If we reach here, the user is not allowed to view this invoice
    return "Unauthorized"