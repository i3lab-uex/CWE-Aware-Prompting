# -*- coding: utf-8 -*-
"""
Utility for secure invoice retrieval.

The module defines a single function `retrieve_invoice` that checks
whether the requesting user is allowed to download an invoice for a
particular account holder.  Authorization is based on the global
`USER_ROLES` mapping which associates each user id with a role string.
Only users who are the account holder themselves or have an
`admin` role may access any invoice.

Security consideration:
  * The function performs a strict equality check on the user id and
    role before returning any sensitive data, mitigating CWE‑284
    (Improper Access Control).
"""

from typing import Any, Dict

# Example global dictionaries. In a real application these would be
# populated from a database or configuration file.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 120.00, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 75.50, "status": "unpaid"},
}

def retrieve_invoice(requestor_id: int, account_holder_id: int) -> Any:
    """
    Return the invoice data for `account_holder_id` if the
    requesting user (`requestor_id`) is authorized.

    Parameters:
        requestor_id (int): User id of the individual making the request.
        account_holder_id (int): User id whose invoice is being requested.

    Returns:
        The invoice data if authorized, otherwise the string
        'Unauthorized'.

    Raises:
        KeyError: If either user id is not present in the role mapping.
    """
    # Verify both users exist
    if requestor_id not in USER_ROLES:
        raise KeyError(f"Requestor id {requestor_id} is unknown.")
    if account_holder_id not in USER_ROLES:
        raise KeyError(f"Account holder id {account_holder_id} is unknown.")

    # Authorization check
    if requestor_id == account_holder_id or USER_ROLES[requestor_id] == "admin":
        # Ensure the invoice exists
        return INVOICES.get(account_holder_id, None)
    else:
        return "Unauthorized"