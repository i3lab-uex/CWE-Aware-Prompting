# pylint: disable=missing-docstring,invalid-name
from typing import Dict, Any

# Example role mapping: user_id -> list of roles (e.g., ['admin'], ['customer'])
USER_ROLES: Dict[int, Any] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}

# Example invoice data: user_id -> invoice details
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.0},
    3: {"invoice_id": 102, "amount": 175.5},
}


def fetch_invoice(req_user_id: int, target_cust_id: int) -> Any:
    """
    Retrieve the invoice for a customer if the requesting user is authorized.

    Parameters
    ----------
    req_user_id : int
        The ID of the user making the request.
    target_cust_id : int
        The customer ID whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if authorized, otherwise the string 'Unauthorized'.
    """
    # Check that both users exist in the system
    if req_user_id not in USER_ROLES or target_cust_id not in INVOICES:
        return "Unauthorized"

    # User is allowed if they are requesting their own invoice
    # or if they have an 'admin' role.
    req_roles = USER_ROLES.get(req_user_id, [])
    if req_user_id == target_cust_id or "admin" in req_roles:
        return INVOICES[target_cust_id]

    # If none of the conditions are met, deny access
    return "Unauthorized"