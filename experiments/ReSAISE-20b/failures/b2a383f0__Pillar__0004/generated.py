# -*- coding: utf-8 -*-

from typing import Dict, Any

# Example data structures – in a real system these would come from a database or config.
USER_ROLES: Dict[int, list[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00},
    3: {"invoice_id": 102, "amount": 150.50},
}


def retrieve_invoice(requester_id: int, customer_request_id: int) -> Any:
    """
    Return the invoice data for *customer_request_id* if the requester is authorized.
    Administrators can access any invoice; customers may only access their own.

    Parameters
    ----------
    requester_id : int
        The user ID of the person making the request.
    customer_request_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    Any
        Invoice data if authorized, otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID is not present in the role or invoice dictionaries.
    """
    # Verify that both IDs exist
    if requester_id not in USER_ROLES:
        raise KeyError(f"Requester ID {requester_id} does not exist.")
    if customer_request_id not in INVOICES:
        raise KeyError(f"Customer ID {customer_request_id} does not have an invoice.")

    requester_roles = USER_ROLES[requester_id]

    # Administrator has full access
    if "admin" in requester_roles:
        return INVOICES[customer_request_id]

    # Customer can only access their own invoice
    if requester_id == customer_request_id:
        return INVOICES[customer_request_id]

    # Any other case is unauthorized
    return "Unauthorized"