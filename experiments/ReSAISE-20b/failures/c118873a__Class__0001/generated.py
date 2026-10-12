# -*- coding: utf-8 -*-

"""
Invoice retrieval module.

This module defines a single function, `retrieve_invoice`, that checks whether
the requesting user is authorized to access a given invoice.  Authorization
is based on two rules:

1. If the user has an "admin" role, they may retrieve any invoice.
2. If the user is the owner of the invoice, they may retrieve it.

The function returns the invoice data if access is permitted; otherwise it
returns the string "Unauthorized".

CWE-862 (Missing Authorization) is mitigated by performing an explicit
authorization check before accessing the invoice data.
"""

from __future__ import annotations

# Example role mapping: user_id -> set of roles
USER_ROLES = {
    1: {"admin"},
    2: {"customer"},
    3: {"customer"},
}

# Example invoice mapping: user_id -> invoice data
INVOICES = {
    2: {"invoice_id": "INV-001", "amount": 100.0, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 200.0, "status": "unpaid"},
}


def retrieve_invoice(logged_in_user_id: int, invoice_owner_id: int) -> dict | str:
    """
    Retrieve an invoice if the requesting user is authorized.

    Parameters
    ----------
    logged_in_user_id : int
        The ID of the user making the request.
    invoice_owner_id : int
        The ID of the customer who owns the requested invoice.

    Returns
    -------
    dict | str
        The invoice data if authorized; otherwise the string "Unauthorized".
    """
    # Basic input validation
    if not isinstance(logged_in_user_id, int) or not isinstance(invoice_owner_id, int):
        raise ValueError("User IDs must be integers.")

    # Fetch roles for the requesting user
    user_roles = USER_ROLES.get(logged_in_user_id, set())

    # Check for admin privilege or ownership
    is_admin = "admin" in user_roles
    is_owner = logged_in_user_id == invoice_owner_id

    if not (is_admin or is_owner):
        return "Unauthorized"

    # Retrieve the invoice data
    invoice = INVOICES.get(invoice_owner_id)
    if invoice is None:
        return "Unauthorized"  # No such invoice or access denied

    return invoice