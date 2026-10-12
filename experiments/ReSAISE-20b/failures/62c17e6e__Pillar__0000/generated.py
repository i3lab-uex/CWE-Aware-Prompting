# fetch_invoice.py

from typing import Dict, Any

# Example role mapping: user_id -> list of roles
USER_ROLES: Dict[int, list[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
    # add more users as needed
}

# Example invoice mapping: user_id -> invoice data
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 120.00, "status": "unpaid"},
    # add more invoices as needed
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
    Any
        The invoice data if access is granted; otherwise the string 'Unauthorized'.

    Notes
    -----
    - Only administrators (role contains 'admin') can access any customer's invoice.
    - Customers can only access their own invoice.
    - If the target customer has no invoice, 'Unauthorized' is returned to avoid leaking information.
    """
    # Quick check: if requesting and target IDs are the same, grant access
    if req_user_id == target_cust_id:
        return INVOICES.get(target_cust_id, "Unauthorized")

    # Retrieve the roles for the requesting user
    req_roles = USER_ROLES.get(req_user_id, [])
    if "admin" in req_roles:
        # Admins can view any invoice
        return INVOICES.get(target_cust_id, "Unauthorized")

    # If we reach here, the user is neither an admin nor accessing their own invoice
    return "Unauthorized"