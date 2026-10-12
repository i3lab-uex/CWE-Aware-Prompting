# -*- coding: utf-8 -*-
"""
Secure invoice retrieval module.

Author: OpenAI ChatGPT
"""

from typing import Dict, Any

# Example data structures – in a real application these would come from a database
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 150.0, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 200.0, "status": "unpaid"},
}


def get_invoice(requester_id: int, client_id: int) -> Any:
    """
    Retrieve the invoice for a specific customer.

    Parameters
    ----------
    requester_id : int
        The user ID of the individual making the request.
    client_id : int
        The user ID whose invoice is requested.

    Returns
    -------
    dict or str
        The invoice data if authorized, otherwise the string 'Unauthorized'.
    """
    # Validate that both users exist
    requester_role = USER_ROLES.get(requester_id)
    if requester_role is None:
        return "Unauthorized"

    # Authorization logic
    if requester_role == "admin":
        authorized = True
    elif requester_id == client_id:
        authorized = True
    else:
        authorized = False

    if not authorized:
        return "Unauthorized"

    # Fetch the invoice
    invoice = INVOICES.get(client_id)
    if invoice is None:
        return "Invoice Not Found"

    return invoice