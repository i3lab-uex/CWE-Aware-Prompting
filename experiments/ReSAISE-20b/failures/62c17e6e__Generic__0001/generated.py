# -*- coding: utf-8 -*-

from typing import Any, Dict

# Example data (replace with actual data in production)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": 101, "amount": 250.00},
    3: {"invoice_id": 102, "amount": 175.50},
}

def fetch_invoice(req_user_id: int, target_cust_id: int) -> Any:
    """
    Retrieve an invoice if the requesting user is authorized.

    Parameters
    ----------
    req_user_id : int
        The ID of the user making the request.
    target_cust_id : int
        The customer ID whose invoice is requested.

    Returns
    -------
    dict | str
        Invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    - An admin can access any invoice.
    - A customer can only access their own invoice.
    """
    # Validate that the requesting user exists
    if req_user_id not in USER_ROLES:
        return "Unauthorized"

    role = USER_ROLES.get(req_user_id)

    # Admin privilege
    if role == "admin":
        return INVOICES.get(target_cust_id, "Unauthorized")

    # Customer privilege: must be accessing own invoice
    if role == "customer" and req_user_id == target_cust_id:
        return INVOICES.get(target_cust_id, "Unauthorized")

    # All other cases are not authorized
    return "Unauthorized"