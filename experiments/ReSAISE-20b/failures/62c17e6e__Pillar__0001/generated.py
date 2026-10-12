# -*- coding: utf-8 -*-
"""
Secure invoice retrieval module.

Author: OpenAI ChatGPT
"""

from typing import Any, Dict

# Sample data – in a real application these would come from a database or secure store.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 120.00, "status": "unpaid"},
}

def fetch_invoice(req_user_id: int, target_cust_id: int) -> Any:
    """
    Retrieve an invoice for a customer.

    Parameters
    ----------
    req_user_id : int
        The ID of the user making the request.
    target_cust_id : int
        The customer ID whose invoice is being requested.

    Returns
    -------
    dict or str
        Invoice data if the requester has permission; otherwise the string 'Unauthorized'.

    Raises
    ------
    ValueError
        If either user ID is not found in the system.
    """
    # Validate that both users exist
    if req_user_id not in USER_ROLES:
        raise ValueError(f"Requester user ID {req_user_id} does not exist.")
    if target_cust_id not in INVOICES:
        raise ValueError(f"Target customer ID {target_cust_id} does not exist.")

    # Authorization check
    requester_role = USER_ROLES[req_user_id]
    if req_user_id != target_cust_id and requester_role.lower() != "admin":
        return "Unauthorized"

    # Return a copy to prevent accidental mutation
    invoice = INVOICES[target_cust_id]
    return dict(invoice)

# Example usage (commented out; remove comments to test):
# print(fetch_invoice(1, 2))  # admin accessing customer 2's invoice
# print(fetch_invoice(2, 3))  # customer 2 trying to access customer 3's invoice -> Unauthorized
# print(fetch_invoice(2, 2))  # customer accessing own invoice