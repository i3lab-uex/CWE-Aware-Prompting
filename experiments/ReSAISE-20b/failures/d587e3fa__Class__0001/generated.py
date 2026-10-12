# -*- coding: utf-8 -*-
"""
Access control for invoice retrieval.

The function ensures that only the owner of an invoice or a user with
the 'admin' role can retrieve it.  It follows the principle of least
privilege and protects against CWE‑862 (Missing Authorization).
"""

from typing import Dict, Any

# Example data – in real usage these would be fetched from a database
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.0, "status": "paid"},
    3: {"invoice_id": 102, "amount": 150.0, "status": "unpaid"},
}


def access_invoice(user_attempt_id: int, cust_id: int) -> Any:
    """
    Retrieve an invoice for a customer if the requesting user is authorized.

    Parameters
    ----------
    user_attempt_id : int
        The ID of the user attempting to access the invoice.
    cust_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice data if access is granted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    * A user can access their own invoice.
    * Users with the role 'admin' can access any invoice.
    * If either the user or the customer does not exist in the
      dictionaries, access is denied.
    """
    # Basic input validation – ensure both IDs are integers
    if not isinstance(user_attempt_id, int) or not isinstance(cust_id, int):
        return "Unauthorized"

    # Verify that the requesting user exists
    role = USER_ROLES.get(user_attempt_id)
    if role is None:
        return "Unauthorized"

    # Owner check
    if user_attempt_id == cust_id:
        invoice = INVOICES.get(cust_id)
        return invoice if invoice is not None else "Unauthorized"

    # Admin privilege check
    if role.lower() == "admin":
        invoice = INVOICES.get(cust_id)
        return invoice if invoice is not None else "Unauthorized"

    # If none of the above, deny access
    return "Unauthorized"