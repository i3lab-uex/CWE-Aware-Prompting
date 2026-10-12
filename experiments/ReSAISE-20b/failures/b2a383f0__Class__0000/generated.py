# -*- coding: utf-8 -*-

from typing import Any, Dict

# Example data structures (should be provided by the surrounding system)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.0},
    3: {"invoice_id": 102, "amount": 175.5},
}


def retrieve_invoice(requester_id: int, customer_request_id: int) -> Any:
    """
    Return the invoice data for a given customer if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the person attempting to access the invoice.
    customer_request_id : int
        The user ID of the customer whose invoice is being requested.

    Returns
    -------
    Any
        The invoice data if access is authorized; otherwise the string 'Unauthorized'.

    Notes
    -----
    Authorization rules:
        * Administrators (role == 'admin') can access any invoice.
        * Customers can only access their own invoice.
    """
    # Retrieve roles safely; default to an empty string if unknown user
    requester_role = USER_ROLES.get(requester_id, "")

    # Check authorization
    if requester_role == "admin" or requester_id == customer_request_id:
        # Return the invoice data if it exists; otherwise treat as unauthorized
        return INVOICES.get(customer_request_id, "Unauthorized")
    else:
        return "Unauthorized"