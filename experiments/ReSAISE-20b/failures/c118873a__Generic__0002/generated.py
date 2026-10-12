# -*- coding: utf-8 -*-
"""
Utility module for invoice retrieval with role‑based access control.
"""

from typing import Any, Dict

# Example data structures (these would normally be populated elsewhere)
USER_ROLES: Dict[int, list[str]] = {
    # user_id : [role1, role2, ...]
}
INVOICES: Dict[int, Any] = {
    # user_id : invoice_data
}


def retrieve_invoice(logged_in_user_id: int, invoice_owner_id: int) -> Any:
    """
    Retrieve an invoice for a given customer if the requesting user has permission.

    Parameters
    ----------
    logged_in_user_id : int
        ID of the user attempting to access the invoice.
    invoice_owner_id : int
        ID of the customer whose invoice is being requested.

    Returns
    -------
    Any
        The invoice data if access is permitted, otherwise the string 'Unauthorized'.

    Notes
    -----
    - Users with the role 'admin' may access any invoice.
    - Regular users may only access their own invoices.
    """
    # Basic type validation
    if not isinstance(logged_in_user_id, int) or not isinstance(invoice_owner_id, int):
        raise ValueError("User IDs must be integers")

    # Fetch roles; if user not found, treat as no role
    user_roles = USER_ROLES.get(logged_in_user_id, [])

    # Admin privilege check
    if "admin" in user_roles:
        return INVOICES.get(invoice_owner_id, "Unauthorized")

    # Ownership check
    if logged_in_user_id == invoice_owner_id:
        return INVOICES.get(invoice_owner_id, "Unauthorized")

    # Default denial
    return "Unauthorized"