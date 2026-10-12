# -*- coding: utf-8 -*-
"""
Utility module for invoice retrieval with proper authorization checks.

The module defines a single function `fetch_invoice` that allows
customers to retrieve only their own invoice, while administrators
can access any customer's invoice.

Author: OpenAI ChatGPT
"""

from typing import Any, Dict

# Example data – in a real application these would come from a database
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": 101, "amount": 250.0},
    3: {"invoice_id": 102, "amount": 175.5},
}


def fetch_invoice(req_user_id: int, target_cust_id: int) -> Any:
    """
    Retrieve an invoice for a customer if the requesting user is authorized.

    Parameters
    ----------
    req_user_id : int
        The ID of the user making the request.
    target_cust_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if the user is authorized, otherwise 'Unauthorized'.

    Notes
    -----
    - Administrators (role == 'admin') can access any invoice.
    - Customers can only access their own invoice.
    - The function performs a strict equality check on roles to avoid
      accidental privilege escalation.

    Raises
    ------
    None

    """
    # Retrieve the role of the requesting user; default to an empty string
    req_role = USER_ROLES.get(req_user_id, "").lower()

    # Authorization check
    if req_role != "admin" and req_user_id != target_cust_id:
        return "Unauthorized"

    # Retrieve the invoice; if not found, still return 'Unauthorized'
    invoice = INVOICES.get(target_cust_id)
    if invoice is None:
        return "Unauthorized"

    return invoice