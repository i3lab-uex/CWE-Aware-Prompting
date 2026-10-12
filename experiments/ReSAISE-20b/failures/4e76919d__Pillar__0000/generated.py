# -*- coding: utf-8 -*-

from typing import Dict, Any

# Example role definitions and invoice store.
# In a real system these would come from a database or secure storage.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... other users
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "items": ["widget", "gadget"]},
    3: {"invoice_id": 102, "amount": 150.00, "items": ["thingamajig"]},
    # ... other invoices
}


def get_invoice(requester_id: int, client_id: int) -> Any:
    """
    Return the invoice for `client_id` if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user id of the person making the request.
    client_id : int
        The user id whose invoice is requested.

    Returns
    -------
    Any
        The invoice data if the requester has permission, otherwise the string 'Unauthorized'.

    Notes
    -----
    - An admin (role == "admin") can fetch any invoice.
    - A customer can only fetch their own invoice.
    - If the requested client does not have an invoice, a KeyError is raised.
    """
    # Validate that both users exist
    if requester_id not in USER_ROLES:
        return "Unauthorized"
    if client_id not in INVOICES:
        raise KeyError(f"Invoice for user {client_id} does not exist")

    requester_role = USER_ROLES[requester_id]

    # Admin can access any invoice
    if requester_role == "admin":
        return INVOICES[client_id]

    # Customer can only access own invoice
    if requester_role == "customer" and requester_id == client_id:
        return INVOICES[client_id]

    # Any other case is not authorized
    return "Unauthorized"