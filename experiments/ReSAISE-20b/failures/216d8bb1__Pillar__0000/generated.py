# -*- coding: utf-8 -*-
"""
Access control for invoice retrieval.

This module defines a single function, `access_invoice`, which enforces
proper access control based on user roles.  The implementation follows the
principle of least privilege: a regular customer may only retrieve their own
invoice, whereas an administrator can access any invoice.

The function is intentionally simple but robust:
* It validates input types.
* It checks the user's role against a predefined mapping.
* It looks up the invoice data from a secure dictionary.
* It returns the invoice details if access is granted, otherwise it
  returns the string 'Unauthorized'.

Author: ChatGPT (2026)
"""

from typing import Dict, Any

# Example role mapping; in a real system this would come from a database or
# authentication service.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... other users
}

# Example invoice storage; in practice this would be a database query.
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 125.00, "status": "unpaid"},
    # ... other invoices
}


def access_invoice(user_id: int, client_id: int) -> Any:
    """
    Retrieve invoice details for a given user and client.

    Parameters
    ----------
    user_id : int
        The ID of the user attempting to retrieve an invoice.
    client_id : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    dict or str
        The invoice data if the user has permission, otherwise 'Unauthorized'.

    Notes
    -----
    * A customer can only access their own invoice.
    * An administrator (role 'admin') can access any customer's invoice.
    """
    # Basic type validation
    if not isinstance(user_id, int) or not isinstance(client_id, int):
        raise TypeError("user_id and client_id must be integers")

    # Determine the user's role; default to 'customer' if not found
    user_role = USER_ROLES.get(user_id, "customer")

    # Check permissions: admin can access any invoice; otherwise must be the owner
    if user_role != "admin" and user_id != client_id:
        return "Unauthorized"

    # Retrieve the invoice; if it does not exist, raise an error
    invoice = INVOICES.get(client_id)
    if invoice is None:
        raise KeyError(f"No invoice found for client_id {client_id}")

    return invoice