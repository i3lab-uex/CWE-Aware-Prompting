# -*- coding: utf-8 -*-
"""
Invoice retrieval module.

Provides a single function `get_invoice` that checks whether the requesting user
has permission to download an invoice.  Administrators may retrieve any
invoice, while regular customers can only access their own.

The module uses two dictionaries:

* USER_ROLES: maps user_id to a string role, e.g. "admin" or "customer".
* INVOICES: maps user_id to the invoice payload (any JSON‑serialisable data).

The function returns the invoice data if authorized, otherwise it returns
the string 'Unauthorized'.
"""

from __future__ import annotations

# Example data structures – replace with real data sources in production.
USER_ROLES = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... more users
}

INVOICES = {
    2: {"invoice_id": "INV-1001", "amount": 250.0, "currency": "USD"},
    3: {"invoice_id": "INV-1002", "amount": 175.5, "currency": "USD"},
    # ... more invoices
}


def get_invoice(requester_id: int, client_id: int):
    """
    Retrieve an invoice if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the person making the request.
    client_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if the requester is authorized, otherwise the string
        'Unauthorized'.

    Notes
    -----
    * Only users with role "admin" may request any invoice.
    * Regular customers may only request their own invoice (requester_id ==
      client_id).
    * If the requested invoice does not exist, None is returned.
    """
    # Basic type checks – defensive programming
    if not isinstance(requester_id, int) or not isinstance(client_id, int):
        raise TypeError("requester_id and client_id must be integers")

    # Determine requester role
    role = USER_ROLES.get(requester_id)
    if role is None:
        # Unknown user – treat as unauthorized
        return "Unauthorized"

    # Authorization logic
    if role == "admin" or requester_id == client_id:
        return INVOICES.get(client_id)

    # If none of the conditions match, deny access
    return "Unauthorized"