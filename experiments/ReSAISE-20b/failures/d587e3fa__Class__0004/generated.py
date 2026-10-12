# -*- coding: utf-8 -*-

"""
Access control for customer invoices.

This module defines a single function `access_invoice` that checks whether
the user attempting to access an invoice is either the owner of that
invoice or has administrative privileges.

The implementation follows best practices for security and
protects against the CWE-862 Missing Authorization vulnerability.
"""

from typing import Any, Dict

# Example role and invoice data structures
USER_ROLES: Dict[int, str] = {
    # user_id : role ('admin' or 'customer')
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Dict[str, Any]] = {
    # user_id : invoice details
    2: {"invoice_id": 101, "amount": 250.0},
    3: {"invoice_id": 102, "amount": 340.5},
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
        The invoice dictionary if access is granted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    - A user can access their own invoice.
    - Users with the role 'admin' can access any customer's invoice.
    - All other attempts are denied.

    Raises
    ------
    KeyError
        If either `user_attempt_id` or `cust_id` is not present in the role
        mapping or invoice database. This helps surface configuration errors.
    """
    # Validate that the user attempting exists
    if user_attempt_id not in USER_ROLES:
        raise KeyError(f"Unknown user attempting access: {user_attempt_id}")

    # Validate that the target customer exists
    if cust_id not in INVOICES:
        raise KeyError(f"Invoice for unknown customer: {cust_id}")

    # Authorization check
    role = USER_ROLES[user_attempt_id]
    if user_attempt_id == cust_id or role.lower() == "admin":
        return INVOICES[cust_id]

    # Deny access if neither condition is met
    return "Unauthorized"