# -*- coding: utf-8 -*-

"""
Secure invoice retrieval module.
"""

from typing import Any, Dict

# Example data structures – in a real system these would be populated from a database
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-1001", "amount": 250.0, "items": ["Widget A", "Widget B"]},
    3: {"invoice_id": "INV-1002", "amount": 150.0, "items": ["Widget C"]},
}


def get_invoice(requester_id: int, client_id: int) -> Any:
    """
    Retrieve the invoice for ``client_id`` if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user id of the individual making the request.
    client_id : int
        The user id whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if the requester is authorized; otherwise the string
        ``"Unauthorized"``.

    Notes
    -----
    * Only users with the role 'admin' can access any invoice.
    * A customer may only access their own invoice.
    * If either user id is not present in the role mapping or the invoice does
      not exist, access is denied.
    """
    # Verify both users exist in the role mapping
    requester_role = USER_ROLES.get(requester_id)
    if requester_role is None:
        return "Unauthorized"

    # Admins can access any invoice
    if requester_role == "admin":
        return INVOICES.get(client_id, "Unauthorized")

    # Customers can only access their own invoice
    if requester_role == "customer" and requester_id == client_id:
        return INVOICES.get(client_id, "Unauthorized")

    # All other cases are unauthorized
    return "Unauthorized"