# -*- coding: utf-8 -*-
"""
Invoice retrieval with role‑based access control.

This module defines `fetch_invoice` which checks that the requester is either
the owner of the invoice or has an administrator role before returning
the invoice data.  The implementation protects against CWE‑862 (Missing
Authorization) by performing an explicit authorization check.
"""

from typing import Any, Dict

# Example data structures – in a real system these would be replaced
# by database look‑ups or other persistence mechanisms.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 120.50, "items": ["Widget A"]},
    3: {"invoice_id": "INV-002", "amount": 75.00,   "items": ["Widget B"]},
}


def fetch_invoice(requester_id: int, owner_id: int) -> Any:
    """
    Retrieve the invoice for `owner_id` if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The ID of the user attempting to access the invoice.
    owner_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    Any
        The invoice data if the requester has permission, otherwise the string
        'Unauthorized'.

    Notes
    -----
    * A user is authorized if they are the owner of the invoice or if their
      role is 'admin'.
    * Missing entries in USER_ROLES or INVOICES are treated as a denial.
    """
    # 1. Quick check for missing data – treat as unauthorized to avoid leaking info.
    if requester_id not in USER_ROLES or owner_id not in INVOICES:
        return "Unauthorized"

    # 2. Role based authorization
    requester_role = USER_ROLES[requester_id]
    if requester_role != "admin" and requester_id != owner_id:
        return "Unauthorized"

    # 3. Return the invoice data
    return INVOICES[owner_id]


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(fetch_invoice(1, 2))   # admin fetching someone else's invoice
#     print(fetch_invoice(2, 2))   # owner fetching own invoice
#     print(fetch_invoice(3, 2))   # unauthorized access attempt