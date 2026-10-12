# -*- coding: utf-8 -*-
"""
retrieve_invoice module

This module defines a function that allows users to retrieve invoices
while enforcing proper authorization checks.

Author: ChatGPT
"""

from typing import Any, Dict

# Example role mapping. In a real system this would be fetched from a database or
# an authentication service.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # Add more users as needed
}

# Example invoice data. Each key is a user_id and the value holds invoice details.
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-1001", "amount": 250.00, "status": "paid"},
    3: {"invoice_id": "INV-1002", "amount": 125.50, "status": "unpaid"},
    # Add more invoices as needed
}


def retrieve_invoice(logged_in_user_id: int, invoice_owner_id: int) -> Any:
    """
    Retrieve an invoice if the requesting user is authorized.

    Parameters
    ----------
    logged_in_user_id : int
        The ID of the user attempting to access an invoice.
    invoice_owner_id : int
        The ID of the customer who owns the invoice.

    Returns
    -------
    dict or str
        The invoice details if access is granted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    * Administrators (role == "admin") may retrieve any invoice.
    * Regular customers may only retrieve their own invoices.
    * If either user ID is unknown, the function returns 'Unauthorized'.
    """
    # Verify that both users exist in the role mapping
    if logged_in_user_id not in USER_ROLES or invoice_owner_id not in USER_ROLES:
        return "Unauthorized"

    # Fetch the role of the logged-in user
    requester_role = USER_ROLES[logged_in_user_id]

    # Authorization logic
    if requester_role == "admin" or logged_in_user_id == invoice_owner_id:
        # Check that the requested invoice exists
        if invoice_owner_id in INVOICES:
            return INVOICES[invoice_owner_id]
    # If we reach this point, the user is not authorized
    return "Unauthorized"