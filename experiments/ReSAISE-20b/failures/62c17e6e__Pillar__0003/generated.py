# -*- coding: utf-8 -*-
"""
Implementation of a secure invoice retrieval function.

Author: OpenAI ChatGPT
"""

from typing import Any, Dict

# Example data structures – in a real system these would come from a database.
USER_ROLES: Dict[int, list[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
    # Add more users as needed
}

INVOICES: Dict[int, dict[str, Any]] = {
    2: {"invoice_id": "INV-1001", "amount": 250.0, "items": ["widget", "gadget"]},
    3: {"invoice_id": "INV-1002", "amount": 125.5, "items": ["widget"]},
    # Add more invoices as needed
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
        The invoice data if authorized; otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user can access their own invoice.
    - Users with the role 'admin' can access any customer's invoice.
    - All other cases are denied to prevent CWE-284: Improper Access Control.
    """
    # Check if the requesting user exists
    req_roles = USER_ROLES.get(req_user_id)
    if req_roles is None:
        return "Unauthorized"

    # Determine authorization
    authorized = False
    if req_user_id == target_cust_id:
        authorized = True
    elif "admin" in (role.lower() for role in req_roles):
        authorized = True

    if not authorized:
        return "Unauthorized"

    # Retrieve the invoice
    invoice = INVOICES.get(target_cust_id)
    if invoice is None:
        return "Unauthorized"  # No invoice exists for the target customer

    return invoice