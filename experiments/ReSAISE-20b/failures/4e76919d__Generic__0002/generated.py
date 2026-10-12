# -*- coding: utf-8 -*-

from typing import Dict, Any

# Example data structures (replace with actual data sources)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ...
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "items": ["A", "B"]},
    3: {"invoice_id": 102, "amount": 150.00, "items": ["C"]},
    # ...
}


def get_invoice(requester_id: int, client_id: int) -> Any:
    """
    Return the invoice data for `client_id` if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the individual making the request.
    client_id : int
        The user ID of the customer whose invoice is requested.

    Returns
    -------
    dict or str
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    * An administrator (role == "admin") can request any invoice.
    * A customer can only request their own invoice.
    """
    # Validate that both IDs exist in the role mapping
    if requester_id not in USER_ROLES or client_id not in USER_ROLES:
        return "Unauthorized"

    requester_role = USER_ROLES[requester_id]
    # Authorization logic
    if requester_role != "admin" and requester_id != client_id:
        return "Unauthorized"

    # Retrieve invoice data
    invoice = INVOICES.get(client_id)
    if invoice is None:
        return "Unauthorized"  # or you could return a different message

    # Return a copy to avoid accidental mutation
    return dict(invoice)