# SPDX-License-Identifier: MIT

from typing import Dict, Any


# Example data – in a real system these would come from a database
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": 101, "amount": 250.0, "status": "paid"},
    3: {"invoice_id": 102, "amount": 125.0, "status": "unpaid"},
}


def fetch_invoice(req_user_id: int, target_cust_id: int) -> Any:
    """
    Return the invoice data for `target_cust_id` if the requesting user
    is authorized.  Authorization rules:

    * Admins (role == "admin") can access any invoice.
    * Customers can only access their own invoice.

    Parameters
    ----------
    req_user_id : int
        ID of the user making the request.
    target_cust_id : int
        ID of the customer whose invoice is requested.

    Returns
    -------
    dict | str
        Invoice data if authorized, otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID is not present in the data stores.
    """
    # Validate that both users exist
    if req_user_id not in USER_ROLES:
        raise KeyError(f"Requesting user {req_user_id} does not exist.")
    if target_cust_id not in INVOICES:
        raise KeyError(f"Target customer {target_cust_id} has no invoice.")

    # Check authorization
    role = USER_ROLES[req_user_id]
    if role == "admin" or req_user_id == target_cust_id:
        return INVOICES[target_cust_id]

    # Unauthorized access
    return "Unauthorized"