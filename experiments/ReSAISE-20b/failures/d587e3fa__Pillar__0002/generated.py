# -*- coding: utf-8 -*-

"""
Access control for invoices.

This module implements a simple authorization check that allows a user to
retrieve only their own invoice, while administrators can retrieve any
customer's invoice.  The implementation follows best practices to avoid
CWE‑284 (Improper Access Control) by explicitly validating the user role
before returning sensitive data.

Author: OpenAI ChatGPT
"""

# --------------------------------------------------------------------------- #
#  Imports
# --------------------------------------------------------------------------- #

from typing import Dict, Any

# --------------------------------------------------------------------------- #
#  Sample data structures
# --------------------------------------------------------------------------- #

# USER_ROLES maps a user_id to a set of roles.
USER_ROLES: Dict[int, set[str]] = {
    1: {"admin"},
    2: {"customer"},
    3: {"customer"},
    # Add more users as needed
}

# INVOICES maps a user_id to their invoice data.
INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": "INV-001", "amount": 120.00, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 75.50, "status": "unpaid"},
    # Add more invoices as needed
}

# --------------------------------------------------------------------------- #
#  Core function
# --------------------------------------------------------------------------- #

def access_invoice(user_attempt_id: int, cust_id: int) -> Any:
    """
    Return the invoice for `cust_id` if the caller (`user_attempt_id`) is authorized.

    Parameters
    ----------
    user_attempt_id : int
        The ID of the user attempting to access an invoice.
    cust_id : int
        The customer ID whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice data if authorized; otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user_attempt_id or cust_id is not present in USER_ROLES or INVOICES.
    """
    # Validate that the user attempting access exists
    if user_attempt_id not in USER_ROLES:
        raise KeyError(f"Unknown user ID: {user_attempt_id}")

    # Validate that the requested customer exists
    if cust_id not in INVOICES:
        raise KeyError(f"Invoice for customer ID {cust_id} does not exist")

    # If the caller is requesting their own invoice, grant access
    if user_attempt_id == cust_id:
        return INVOICES[cust_id]

    # Otherwise, check if the caller has an admin role
    user_roles = USER_ROLES[user_attempt_id]
    if "admin" in user_roles:
        return INVOICES[cust_id]

    # If none of the above, deny access
    return "Unauthorized"

# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     print(access_invoice(1, 2))   # Admin accessing customer 2's invoice
#     print(access_invoice(2, 3))   # Customer accessing another customer's invoice
#     print(access_invoice(2, 2))   # Customer accessing own invoice