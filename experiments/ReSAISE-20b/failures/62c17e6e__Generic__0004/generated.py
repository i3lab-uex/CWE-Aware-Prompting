# ------------------------------------------------------------
# Invoice access control module
# ------------------------------------------------------------

from typing import Any, Dict

# Example role and invoice data (these would normally come from a database)
USER_ROLES: Dict[int, set[str]] = {
    1: {"customer"},
    2: {"admin"},
    3: {"customer"},
}

INVOICES: Dict[int, Any] = {
    1: {"invoice_id": 101, "amount": 250.0},
    3: {"invoice_id": 102, "amount": 180.5},
}

def fetch_invoice(req_user_id: int, target_cust_id: int) -> Any:
    """
    Retrieve an invoice for a customer if the requesting user is authorized.

    Parameters
    ----------
    req_user_id : int
        User ID of the person making the request.
    target_cust_id : int
        Customer user ID whose invoice is being requested.

    Returns
    -------
    Any
        Invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    - Administrators (users with role 'admin') can access any customer's invoice.
    - Customers can only access their own invoice.
    """
    # Validate that the requesting user exists
    if req_user_id not in USER_ROLES:
        return "Unauthorized"

    # Admin check
    if "admin" in USER_ROLES[req_user_id]:
        return INVOICES.get(target_cust_id, "Unauthorized")

    # Customer can only access own invoice
    if req_user_id == target_cust_id:
        return INVOICES.get(req_user_id, "Unauthorized")

    # If none of the above conditions are met, deny access
    return "Unauthorized"