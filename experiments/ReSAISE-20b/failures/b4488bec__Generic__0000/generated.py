# -*- coding: utf-8 -*-

"""
Invoice retrieval module.

This module provides the `fetch_invoice` function, which allows a user to download
their own invoice or an administrator to download any customer's invoice.
"""

from typing import Any, Dict

# Example role definitions and invoice data
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

INVOICES: Dict[int, str] = {
    2: "Invoice data for user 2",
    3: "Invoice data for user 3",
}

def fetch_invoice(user_id: int, customer: int) -> Any:
    """
    Retrieve the invoice for a given customer if the requesting user is authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user making the request.
    customer : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    str or dict
        The invoice data if the user has permission, otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user can fetch their own invoice.
    - An administrator (role == 'admin') can fetch any customer's invoice.
    - If the requested customer has no invoice, 'Unauthorized' is returned.
    """
    # Basic input validation
    if not isinstance(user_id, int) or not isinstance(customer, int):
        return "Unauthorized"

    # Check if the user exists in the role mapping
    requester_role = USER_ROLES.get(user_id)
    if requester_role is None:
        return "Unauthorized"

    # Determine authorization
    authorized = False
    if requester_role == "admin":
        authorized = True
    elif user_id == customer:
        # Customers can fetch their own invoice
        authorized = True

    if not authorized:
        return "Unauthorized"

    # Fetch the invoice data
    invoice = INVOICES.get(customer)
    if invoice is None:
        return "Unauthorized"

    return invoice