# -*- coding: utf-8 -*-

from typing import Any, Dict

# Example data structures (in real usage these would come from a database or config)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": "INV-001", "amount": 150.0, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 200.0, "status": "unpaid"},
    # Note: admin users typically don't have invoices of their own
}


def retrieve_invoice(requester_id: int, customer_request_id: int) -> Any:
    """
    Return the invoice for *customer_request_id* if *requester_id* is authorized.

    Authorization logic:
        - If requester is an admin (role == "admin") → grant access.
        - Else if requester_id equals customer_request_id → grant access.
        - Otherwise → deny.

    Parameters
    ----------
    requester_id : int
        ID of the user making the request.
    customer_request_id : int
        ID of the customer whose invoice is requested.

    Returns
    -------
    dict or str
        The invoice dictionary if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    - If either user ID is unknown in USER_ROLES or INVOICES, the function
      treats it as an unauthorized request.
    - No exceptions are raised; the caller receives a clear status string.
    """
    # Quick sanity checks
    if requester_id not in USER_ROLES or customer_request_id not in INVOICES:
        return "Unauthorized"

    requester_role = USER_ROLES[requester_id]

    # Authorization check
    if requester_role == "admin" or requester_id == customer_request_id:
        return INVOICES[customer_request_id]

    return "Unauthorized"