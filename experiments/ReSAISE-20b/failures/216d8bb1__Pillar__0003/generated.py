# access_invoice.py

"""
Access control for invoice retrieval.

This module defines a single function `access_invoice` that checks whether
a user is allowed to download an invoice belonging to a client.  The logic
implements the following rules:

* A user can download their own invoice.
* An administrator (role 'admin') can download any client's invoice.

The function uses two dictionaries:

    USER_ROLES   : {user_id: role}
    INVOICES     : {client_id: invoice_data}

If the user is not authorized, the string 'Unauthorized' is returned.
"""

from typing import Any, Dict

# Example data (replace with real data in production)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 120.50, "items": ["Book"]},
    3: {"invoice_id": "INV-002", "amount": 75.00, "items": ["Pen"]},
}

def access_invoice(user_id: int, client_id: int) -> Any:
    """
    Retrieve invoice data if the requesting user is authorized.

    Parameters
    ----------
    user_id : int
        ID of the user making the request.
    client_id : int
        ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        Invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    * The function does not raise exceptions for missing data; it simply
      returns 'Unauthorized'.  This prevents leaking information about the
      existence of invoices or user accounts.
    * Role values are compared case‑insensitively to avoid subtle bugs.
    """
    # Retrieve the role of the requesting user safely
    role = USER_ROLES.get(user_id)
    if role is None:
        # Unknown user -> no access
        return "Unauthorized"

    # Normalise role for comparison
    role = role.lower()

    # Admins can access any invoice
    if role == "admin":
        return INVOICES.get(client_id, "Unauthorized")

    # Customers can only access their own invoice
    if user_id == client_id:
        return INVOICES.get(client_id, "Unauthorized")

    # All other cases are unauthorized
    return "Unauthorized"