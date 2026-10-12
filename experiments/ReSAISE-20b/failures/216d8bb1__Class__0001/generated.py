# -*- coding: utf-8 -*-

from typing import Any, Dict

# Example role mapping (user_id -> role)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

# Example invoice storage (user_id -> invoice data)
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.0, "status": "paid"},
    3: {"invoice_id": 102, "amount": 125.5, "status": "unpaid"},
}


def access_invoice(user_id: int, client_id: int) -> Any:
    """
    Retrieve an invoice for a given client if the requesting user is authorized.

    Parameters
    ----------
    user_id : int
        ID of the user attempting to retrieve an invoice.
    client_id : int
        ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    This function enforces role‑based access control:
        * Administrators can retrieve any invoice.
        * Customers can only retrieve their own invoices.
    """
    # Basic validation
    if not isinstance(user_id, int) or not isinstance(client_id, int):
        raise TypeError("user_id and client_id must be integers")

    # Retrieve the role of the requesting user
    role = USER_ROLES.get(user_id)
    if role is None:
        return "Unauthorized"

    # Administrator bypasses client check
    if role.lower() == "admin":
        invoice = INVOICES.get(client_id)
        return invoice if invoice is not None else "Unauthorized"

    # Customer: can only access own invoice
    if role.lower() == "customer" and user_id == client_id:
        return INVOICES.get(client_id, "Unauthorized")

    # Any other case is forbidden
    return "Unauthorized"