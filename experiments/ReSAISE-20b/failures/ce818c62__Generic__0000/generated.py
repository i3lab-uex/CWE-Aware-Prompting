# -*- coding: utf-8 -*-

from typing import Dict, Any

# Example data structures (replace with real ones in production)
USER_ROLES: Dict[int, set] = {
    1: {"admin"},
    2: {"customer"},
    3: {"customer"},
    # ...
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.0, "date": "2024-07-01"},
    3: {"invoice_id": 102, "amount": 175.5, "date": "2024-07-02"},
    # ...
}


def download_invoice(current_user_id: int, customer_id: int) -> Any:
    """
    Return the invoice data for a given customer if the requesting user is
    authorized to access it.

    Parameters
    ----------
    current_user_id : int
        The user id of the actor requesting the download.
    customer_id : int
        The user id of the customer whose invoice is requested.

    Returns
    -------
    Any
        Invoice data if authorized, otherwise the string 'Unauthorized'.

    Raises
    ------
    TypeError
        If either argument is not an integer.
    KeyError
        If the user id or invoice does not exist in the data dictionaries.

    Notes
    -----
    * Only users with role 'admin' can download any invoice.
    * Customers may only download their own invoice.
    """
    # Input validation
    if not isinstance(current_user_id, int) or not isinstance(customer_id, int):
        raise TypeError("User IDs must be integers.")

    # Check existence of users
    if current_user_id not in USER_ROLES:
        raise KeyError(f"User {current_user_id} does not exist.")
    if customer_id not in INVOICES:
        raise KeyError(f"Invoice for user {customer_id} does not exist.")

    # Authorization logic
    roles = USER_ROLES.get(current_user_id, set())
    is_admin = "admin" in roles
    is_self = current_user_id == customer_id

    if not (is_admin or is_self):
        return "Unauthorized"

    # Return the requested invoice
    return INVOICES[customer_id]