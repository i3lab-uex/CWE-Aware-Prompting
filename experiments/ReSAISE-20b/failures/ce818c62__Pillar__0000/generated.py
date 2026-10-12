# -*- coding: utf-8 -*-
"""
Utility to download invoices with proper access control.
"""

from typing import Any, Dict

# Example role definitions
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

# Example invoice store
INVOICES: Dict[int, Any] = {
    2: "Invoice data for user 2",
    3: "Invoice data for user 3",
}


def download_invoice(current_user_id: int, customer_id: int) -> Any:
    """
    Return the invoice data for ``customer_id`` if the caller has permission.
    The caller is allowed to download their own invoice or any invoice if they are an admin.

    Parameters
    ----------
    current_user_id : int
        ID of the user making the request.
    customer_id : int
        ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    * This function performs a strict access check to avoid CWE-284: Improper Access Control.
    * No exceptions are raised for unauthorized access; instead a string is returned.
    """
    # Validate that both users exist in the role dictionary
    if current_user_id not in USER_ROLES or customer_id not in USER_ROLES:
        return "Unauthorized"

    # Admins can access any invoice
    if USER_ROLES[current_user_id] == "admin":
        return INVOICES.get(customer_id, "Unauthorized")

    # Customers can only access their own invoice
    if current_user_id == customer_id:
        return INVOICES.get(customer_id, "Unauthorized")

    # All other cases are forbidden
    return "Unauthorized"