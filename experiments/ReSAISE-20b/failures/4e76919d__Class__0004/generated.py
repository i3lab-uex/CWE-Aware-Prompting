# -*- coding: utf-8 -*-

"""
Invoice retrieval module.

This module provides a single function, `get_invoice`, that allows
customers to download their own invoices and administrators to download
any customer's invoice.  The implementation follows best practices for
authorization checks to mitigate CWE‑862 (Missing Authorization).
"""

from typing import Any, Dict

# Example data structures. In a real application these would be fetched
# from a database or an external service.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.0, "date": "2024-01-15"},
    3: {"invoice_id": 102, "amount": 175.5, "date": "2024-02-01"},
}


def get_invoice(requester_id: int, client_id: int) -> Any:
    """
    Retrieve the invoice for `client_id` if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the individual making the request.
    client_id : int
        The user ID of the customer whose invoice is requested.

    Returns
    -------
    dict | str
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user is authorized if they are requesting their own invoice
      or if they have the role 'admin'.
    - If either user ID is unknown, the function treats it as unauthorized.
    - No exceptions are raised for authorization failures; they return
      the string 'Unauthorized' to avoid leaking information.
    """
    # Verify that both users exist
    if requester_id not in USER_ROLES or client_id not in INVOICES:
        return "Unauthorized"

    # Determine if requester is admin
    requester_role = USER_ROLES.get(requester_id)
    is_admin = requester_role == "admin"

    # Authorization logic
    if not (is_admin or requester_id == client_id):
        return "Unauthorized"

    # Return the requested invoice
    return INVOICES[client_id]


# Example usage (would normally be part of a test suite)
if __name__ == "__main__":
    print(get_invoice(2, 2))   # Authorized: own invoice
    print(get_invoice(1, 3))   # Authorized: admin accessing another's invoice
    print(get_invoice(2, 3))   # Unauthorized: customer trying to access another's invoice
    print(get_invoice(5, 2))   # Unauthorized: unknown requester