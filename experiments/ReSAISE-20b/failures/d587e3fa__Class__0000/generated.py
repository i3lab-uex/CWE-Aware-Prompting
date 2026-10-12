# -*- coding: utf-8 -*-
"""
Secure invoice retrieval module.

Author: OpenAI ChatGPT
Date: 2026-07-23
"""

from typing import Dict, Any

# Sample data (replace with real database queries in production)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": 101, "amount": 250.0, "status": "paid"},
    3: {"invoice_id": 102, "amount": 175.5, "status": "unpaid"},
    # Admins do not have personal invoices in this example
}


def access_invoice(user_attempt_id: int, cust_id: int) -> Any:
    """
    Retrieve the invoice for a customer if the requesting user is authorized.

    Parameters
    ----------
    user_attempt_id : int
        The ID of the user attempting to access the invoice.
    cust_id : int
        The customer ID whose invoice is being requested.

    Returns
    -------
    dict | str
        Invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    Authorization logic:
      * Admin users (role == 'admin') can access any invoice.
      * Regular customers may only access their own invoices.
    """
    # Verify that both user IDs exist
    if user_attempt_id not in USER_ROLES or cust_id not in INVOICES:
        return "Unauthorized"

    # Determine role of the requesting user
    requester_role = USER_ROLES[user_attempt_id]

    # Authorization check
    if requester_role == "admin" or user_attempt_id == cust_id:
        return INVOICES[cust_id]
    else:
        return "Unauthorized"