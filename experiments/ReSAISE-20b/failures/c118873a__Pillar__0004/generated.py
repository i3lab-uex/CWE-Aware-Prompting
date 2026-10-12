# -*- coding: utf-8 -*-

"""
Module providing secure invoice retrieval functionality.
"""

from __future__ import annotations

from typing import Dict, Any


# Example data structures. In a real system these would come from
# a database or an external service.
USER_ROLES: Dict[int, set[str]] = {
    1: {"customer"},
    2: {"admin"},
    3: {"customer"},
}

INVOICES: Dict[int, Any] = {
    1: {"invoice_id": "INV-001", "amount": 120.00, "currency": "USD"},
    3: {"invoice_id": "INV-003", "amount": 75.50, "currency": "USD"},
}


def retrieve_invoice(logged_in_user_id: int, invoice_owner_id: int) -> Any:
    """
    Retrieve an invoice for a given owner if the logged-in user has
    sufficient privileges.

    Parameters
    ----------
    logged_in_user_id : int
        The ID of the user attempting to retrieve the invoice.
    invoice_owner_id : int
        The ID of the customer who owns the invoice.

    Returns
    -------
    dict | str
        The invoice details if access is granted; otherwise the string
        'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID is not present in USER_ROLES.
    """
    # Validate that the requesting user exists
    if logged_in_user_id not in USER_ROLES:
        raise KeyError(f"User ID {logged_in_user_id} does not exist.")

    # Determine if the user has admin privileges
    is_admin = "admin" in USER_ROLES[logged_in_user_id]

    # Allow access if user is admin or owner of the invoice
    if not (is_admin or logged_in_user_id == invoice_owner_id):
        return "Unauthorized"

    # Retrieve the invoice data; if not found, return None or raise an error
    invoice = INVOICES.get(invoice_owner_id)
    if invoice is None:
        return "Unauthorized"  # No invoice found for the owner

    return invoice