# -*- coding: utf-8 -*-
"""
Invoice retrieval module.

This module defines a single function `retrieve_invoice` that
enforces role‑based access control.  The function allows:

* **Administrators** to download any invoice.
* **Customers** to download only their own invoice.

The implementation follows the principles of least privilege and
protects against CWE‑862 (Missing Authorization) by performing a
strict role check before returning the invoice data.
"""

from __future__ import annotations

# Sample user roles and invoices for demonstration purposes
USER_ROLES = {
    1: "ADMIN",
    2: "CUSTOMER",
    3: "CUSTOMER",
    # Add more users as needed
}

INVOICES = {
    2: {"invoice_id": "INV-001", "amount": 120.00, "date": "2024‑07‑01"},
    3: {"invoice_id": "INV-002", "amount": 250.00, "date": "2024‑07‑02"},
    # Add more invoices as needed
}

def retrieve_invoice(requestor_id: int, account_holder_id: int):
    """
    Retrieve the invoice for a given customer if the requestor is authorized.

    Parameters
    ----------
    requestor_id : int
        The user ID of the individual requesting the invoice.
    account_holder_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    dict | str
        Invoice data if authorized; otherwise the string 'Unauthorized'.

    Notes
    -----
    * An ADMIN can retrieve any invoice.
    * A CUSTOMER can only retrieve their own invoice.
    * If either user ID is unknown, the function returns 'Unauthorized'.
    """
    # Validate that both IDs exist in the system
    if requestor_id not in USER_ROLES or account_holder_id not in INVOICES:
        return "Unauthorized"

    # Determine requestor's role
    role = USER_ROLES.get(requestor_id)

    # Authorization logic
    if role == "ADMIN":
        return INVOICES[account_holder_id]
    elif role == "CUSTOMER" and requestor_id == account_holder_id:
        return INVOICES[account_holder_id]
    else:
        return "Unauthorized"

# Example usage (uncomment to test)
# print(retrieve_invoice(1, 2))  # ADMIN accessing customer 2's invoice
# print(retrieve_invoice(2, 2))  # Customer accessing own invoice
# print(retrieve_invoice(2, 3))  # Customer trying to access another's invoice