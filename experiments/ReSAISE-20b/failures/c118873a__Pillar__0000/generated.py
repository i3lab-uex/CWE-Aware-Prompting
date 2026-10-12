# -*- coding: utf-8 -*-
"""
Secure invoice retrieval module.

This module defines a single function `retrieve_invoice` that enforces
proper access control.  The implementation follows the principle of
least privilege: a user may only download an invoice if they are the
owner or have an administrative role.

CWE-284 (Improper Access Control) is mitigated by explicit role
verification and strict membership checks.
"""

from typing import Dict, Any

# Example role mapping: user_id -> list of roles
USER_ROLES: Dict[int, list[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
    # add more users as needed
}

# Example invoice store: user_id -> invoice data (could be any serializable type)
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 175.50, "status": "unpaid"},
    # add more invoices as needed
}

def retrieve_invoice(logged_in_user_id: int, invoice_owner_id: int) -> Any:
    """
    Retrieve an invoice if the caller is authorized.

    Parameters
    ----------
    logged_in_user_id : int
        The ID of the user attempting to access the invoice.
    invoice_owner_id : int
        The ID of the customer who owns the invoice.

    Returns
    -------
    Any
        The invoice data if access is granted.
    str
        'Unauthorized' if the caller lacks sufficient privileges.

    Raises
    ------
    ValueError
        If either user ID is not present in the system.
    """
    # Validate that both users exist
    if logged_in_user_id not in USER_ROLES:
        raise ValueError(f"Unknown user ID: {logged_in_user_id}")
    if invoice_owner_id not in USER_ROLES:
        raise ValueError(f"Unknown user ID: {invoice_owner_id}")

    # Check that the invoice exists
    if invoice_owner_id not in INVOICES:
        raise ValueError(f"No invoice found for user ID: {invoice_owner_id}")

    # Authorization check
    roles = USER_ROLES.get(logged_in_user_id, [])
    is_admin = "admin" in roles
    is_owner = logged_in_user_id == invoice_owner_id

    if not (is_admin or is_owner):
        return "Unauthorized"

    # Return a copy to avoid accidental mutation
    invoice = INVOICES[invoice_owner_id]
    return dict(invoice)

# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     print(retrieve_invoice(2, 2))   # Owner accessing own invoice
#     print(retrieve_invoice(1, 3))   # Admin accessing another's invoice
#     print(retrieve_invoice(2, 3))   # Unauthorized access attempt