# -*- coding: utf-8 -*-

"""
Implementation of the fetch_invoice function with proper authorization checks.
"""

from typing import Dict, Any

# Example data structures – in real code these would come from a database or config
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": 101, "amount": 250.0, "status": "paid"},
    3: {"invoice_id": 102, "amount": 175.5, "status": "unpaid"},
}


def fetch_invoice(req_user_id: int, target_cust_id: int) -> Any:
    """
    Retrieve an invoice for a customer if the requesting user is authorized.

    Parameters
    ----------
    req_user_id : int
        The ID of the user making the request.
    target_cust_id : int
        The customer ID whose invoice is requested.

    Returns
    -------
    dict or str
        Invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    Authorization logic:
      * If the requester is the same as the target customer, access is granted.
      * If the requester has the role 'admin', access to any invoice is granted.
      * All other cases are denied.

    Raises
    ------
    KeyError
        If either the requester or target user ID is not present in USER_ROLES.
    """
    # Ensure the requesting user exists
    if req_user_id not in USER_ROLES:
        raise KeyError(f"Requesting user ID {req_user_id} not found in USER_ROLES")

    # Authorization check
    role = USER_ROLES[req_user_id]
    if req_user_id == target_cust_id or role.lower() == "admin":
        # Ensure the invoice exists for the target customer
        if target_cust_id in INVOICES:
            return INVOICES[target_cust_id]
        else:
            # If no invoice exists, still treat as unauthorized to avoid revealing existence
            return "Unauthorized"
    else:
        return "Unauthorized"


# Example usage (uncomment to test):
# print(fetch_invoice(1, 2))   # Admin accessing customer 2's invoice
# print(fetch_invoice(2, 3))   # Customer 2 trying to access customer 3's invoice
# print(fetch_invoice(2, 2))   # Customer accessing own invoice